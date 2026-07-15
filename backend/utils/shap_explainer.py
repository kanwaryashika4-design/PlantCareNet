import shap
import numpy as np
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO


FEATURE_LABELS = {
    'N': 'Nitrogen (N)',
    'P': 'Phosphorus (P)',
    'K': 'Potassium (K)',
    'temperature': 'Temperature',
    'humidity': 'Humidity',
    'ph': 'Soil pH',
    'yellowing_percentage': 'Yellowing %',
    'green_index': 'Green Index',
    'dry_edge_percentage': 'Dry Edge %'
}

FEATURE_NAMES = [
    'N', 'P', 'K', 'temperature',
    'humidity', 'ph',
    'yellowing_percentage', 'green_index', 'dry_edge_percentage'
]


def generate_shap_chart(model, features_array, prediction_label):
    """
    Generate SHAP waterfall chart for nutrient prediction.
    Returns base64 encoded chart image.
    """
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(features_array)

        # For multi-class, get SHAP values for predicted class
        class_names = list(model.classes_)
        if prediction_label in class_names:
            class_idx = class_names.index(prediction_label)
            if isinstance(shap_values, list):
                values = shap_values[class_idx][0]
            else:
                values = shap_values[0]
        else:
            values = shap_values[0] if not isinstance(
                shap_values, list) else shap_values[0][0]

        # Use only the first 6 real features for display
        display_values = values[:6]
        display_features = FEATURE_NAMES[:6]
        display_labels = [FEATURE_LABELS[f] for f in display_features]
        actual_values = features_array[0][:6]

        # Sort by absolute importance
        sorted_indices = np.argsort(np.abs(display_values))
        sorted_values = display_values[sorted_indices]
        sorted_labels = [
            f"{display_labels[i]}\n= {actual_values[i]:.1f}"
            for i in sorted_indices
        ]

        # Create chart
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')

        colors = ['#c62828' if v > 0 else '#1565c0' for v in sorted_values]
        bars = ax.barh(sorted_labels, sorted_values, color=colors,
                       height=0.55, edgecolor='none')

        # Add value labels on bars
        for bar, val in zip(bars, sorted_values):
            width = bar.get_width()
            x_pos = width + 0.001 if width >= 0 else width - 0.001
            ha = 'left' if width >= 0 else 'right'
            ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                    f'{val:+.3f}', va='center', ha=ha,
                    fontsize=8, color='#333')

        ax.axvline(x=0, color='#555', linewidth=0.8, linestyle='-')
        ax.set_xlabel('SHAP Value (impact on prediction)', fontsize=9,
                      color='#555')
        ax.set_title(
            f'Feature Impact for: {prediction_label.replace("_", " ")}',
            fontsize=10, fontweight='bold', color='#1a1a1a', pad=10
        )

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#c62828', label='Increases deficiency risk'),
            Patch(facecolor='#1565c0', label='Decreases deficiency risk')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=7,
                  framealpha=0.7)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#ddd')
        ax.spines['bottom'].set_color('#ddd')
        ax.tick_params(axis='y', labelsize=8, colors='#333')
        ax.tick_params(axis='x', labelsize=7, colors='#555')

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='PNG', dpi=130,
                    bbox_inches='tight', facecolor='#f8f9fa')
        plt.close(fig)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        print(f"SHAP error: {e}")
        return None