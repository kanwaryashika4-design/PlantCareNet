import numpy as np
import cv2
import tensorflow as tf
import base64
from io import BytesIO
from PIL import Image


def get_last_conv_layer(model):
    """Find the last convolutional layer in MobileNetV2."""
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
    return None


def generate_gradcam(model, img_array, class_index, pil_image):
    """
    Generate Grad-CAM heatmap for the predicted class.
    Returns base64 encoded image of heatmap overlaid on original.
    """
    try:
        last_conv_layer_name = get_last_conv_layer(model)

        if last_conv_layer_name is None:
            return None

        # Build grad model
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[
                model.get_layer(last_conv_layer_name).output,
                model.output
            ]
        )

        with tf.GradientTape() as tape:
            inputs = tf.cast(img_array, tf.float32)
            conv_outputs, predictions = grad_model(inputs)
            loss = predictions[:, class_index]

        # Compute gradients
        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        heatmap = heatmap.numpy()

        # Resize heatmap to original image size
        original_img = np.array(pil_image.convert('RGB'))
        height, width = original_img.shape[:2]

        heatmap_resized = cv2.resize(heatmap, (width, height))
        heatmap_colored = cv2.applyColorMap(
            np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

        # Overlay heatmap on original image
        overlay = cv2.addWeighted(original_img, 0.55, heatmap_colored, 0.45, 0)

        # Add legend bar at bottom
        legend_height = 24
        legend = np.zeros((legend_height, width, 3), dtype=np.uint8)
        for x in range(width):
            val = int(255 * x / width)
            color = cv2.applyColorMap(np.uint8([[val]]), cv2.COLORMAP_JET)[0][0]
            legend[:, x] = color[::-1]

        final_img = np.vstack([overlay, legend])

        # Convert to base64
        pil_result = Image.fromarray(final_img)
        buffer = BytesIO()
        pil_result.save(buffer, format='JPEG', quality=90)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return f"data:image/jpeg;base64,{img_base64}"

    except Exception as e:
        print(f"Grad-CAM error: {e}")
        return None


def get_all_class_probabilities(predictions, class_indices):
    """Return probability for all classes."""
    probs = predictions[0]
    result = []
    for idx, prob in enumerate(probs):
        label = class_indices.get(idx, f"Class {idx}")
        result.append({
            'label': label.replace('_', ' ').title(),
            'probability': round(float(prob) * 100, 2)
        })
    result.sort(key=lambda x: x['probability'], reverse=True)
    return result