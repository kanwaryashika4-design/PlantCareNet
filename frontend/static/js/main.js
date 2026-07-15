// ===== FARMER PORTAL =====

const imageInput = document.getElementById('imageInput');
const uploadArea = document.getElementById('uploadArea');
const uploadPlaceholder = document.getElementById('uploadPlaceholder');
const imagePreviewWrapper = document.getElementById('imagePreviewWrapper');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');

let selectedFile = null;
let lastDiagnosisData = null;

if (imageInput) {
    imageInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) handleFileSelect(file);
    });
}

if (uploadArea) {
    uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    uploadArea.addEventListener('dragleave', function () {
        uploadArea.classList.remove('dragover');
    });
    uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file) handleFileSelect(file);
    });
}

function handleFileSelect(file) {
    const allowed = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowed.includes(file.type)) {
        alert('Please upload a JPG, PNG, or WEBP image.');
        return;
    }
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be under 10MB.');
        return;
    }
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = function (e) {
        if (imagePreview) imagePreview.src = e.target.result;
        if (uploadPlaceholder) uploadPlaceholder.style.display = 'none';
        if (imagePreviewWrapper) imagePreviewWrapper.style.display = 'block';
        if (analyzeBtn) analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

function resetUpload() {
    selectedFile = null;
    lastDiagnosisData = null;
    if (imageInput) imageInput.value = '';
    if (uploadPlaceholder) uploadPlaceholder.style.display = 'block';
    if (imagePreviewWrapper) imagePreviewWrapper.style.display = 'none';
    if (analyzeBtn) analyzeBtn.disabled = true;
    const rs = document.getElementById('resultsSection');
    if (rs) rs.style.display = 'none';
    const fill = document.getElementById('severityBarFill');
    if (fill) fill.style.width = '0%';
}

async function analyzeDiseaseImage() {
    if (!selectedFile) return;

    const resultsSection = document.getElementById('resultsSection');
    const loadingCard = document.getElementById('loadingCard');
    const resultsCard = document.getElementById('resultsCard');
    const errorCard = document.getElementById('errorCard');
    const invalidCard = document.getElementById('invalidCard');

    resultsSection.style.display = 'block';
    loadingCard.style.display = 'block';
    resultsCard.style.display = 'none';
    errorCard.style.display = 'none';
    if (invalidCard) invalidCard.style.display = 'none';

    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        const response = await fetch('/predict/disease', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        loadingCard.style.display = 'none';

        if (data.invalid_image) {
            renderInvalidImage(data);
        } else if (data.success) {
            lastDiagnosisData = data;
            renderDiseaseResults(data);
            resultsCard.style.display = 'block';
        } else {
            document.getElementById('errorText').textContent =
                data.error || 'Analysis failed.';
            errorCard.style.display = 'block';
        }

    } catch (err) {
        loadingCard.style.display = 'none';
        document.getElementById('errorText').textContent =
            'Network error. Please try again.';
        errorCard.style.display = 'block';
    }
}

function renderInvalidImage(data) {
    const invalidCard = document.getElementById('invalidCard');
    if (!invalidCard) return;
    const reasonsEl = document.getElementById('invalidReasons');
    const tipsEl = document.getElementById('invalidTips');
    if (reasonsEl) {
        reasonsEl.innerHTML = data.reasons
            .map(r => `<span class="inv-reason-tag">${r}</span>`)
            .join('');
    }
    if (tipsEl) {
        tipsEl.innerHTML = data.tips.map(t => `<li>${t}</li>`).join('');
    }
    invalidCard.style.display = 'block';
}

function renderDiseaseResults(data) {
    document.getElementById('diseaseResult').textContent = data.disease;
    document.getElementById('confidenceResult').textContent =
        data.confidence + '%';

    const isHealthy = data.is_healthy;

    // Severity section
    const severitySection = document.getElementById('severitySection');
    if (severitySection) {
        severitySection.style.display = isHealthy ? 'none' : 'block';
    }

    if (!isHealthy) {
        const severityPctEl = document.getElementById('severityPctResult');
        if (severityPctEl) {
            severityPctEl.textContent = data.severity_percentage + '%';
        }

        const severityLevelEl = document.getElementById('severityLevelResult');
        if (severityLevelEl) {
            severityLevelEl.textContent = data.severity_level;
            const colorMap = {
                'Mild': '#4caf7d',
                'Moderate': '#ff9800',
                'Severe': '#f44336'
            };
            severityLevelEl.style.background =
                colorMap[data.severity_level] || '#9e9e9e';
            severityLevelEl.style.color = '#fff';
            severityLevelEl.style.padding = '4px 12px';
            severityLevelEl.style.borderRadius = '50px';
        }

        const barPct = document.getElementById('severityBarPct');
        if (barPct) barPct.textContent = data.severity_percentage + '%';

        setTimeout(() => {
            const fill = document.getElementById('severityBarFill');
            if (fill) {
                fill.style.width =
                    Math.min(data.severity_percentage, 100) + '%';
            }
        }, 100);
    }

    // All class probabilities
    const probContainer = document.getElementById('allProbabilities');
    if (probContainer && data.all_probabilities) {
        probContainer.innerHTML = data.all_probabilities.map(item => `
            <div style="margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;
                            font-size:0.78rem;margin-bottom:3px">
                    <span style="color:var(--gray-800);font-weight:500">
                        ${item.label}
                    </span>
                    <span style="color:var(--gray-600)">${item.probability}%</span>
                </div>
                <div style="height:6px;background:var(--gray-200);
                            border-radius:50px;overflow:hidden">
                    <div style="height:100%;width:${item.probability}%;
                                background:${item.probability > 50 ?
                                    'var(--green-600)' : 'var(--gray-400)'};
                                border-radius:50px;transition:width 0.8s ease">
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Grad-CAM
    const gradcamSection = document.getElementById('gradcamSection');
    const gradcamImage = document.getElementById('gradcamImage');
    if (gradcamSection && gradcamImage && data.gradcam_image) {
        gradcamImage.src = data.gradcam_image;
        gradcamSection.style.display = 'block';
    }

    // Treatment
    const treatmentEl = document.getElementById('treatmentText');
    if (treatmentEl) treatmentEl.textContent = data.treatment;

    const priorityBadge = document.getElementById('priorityBadge');
    if (priorityBadge) {
        priorityBadge.textContent = data.priority;
        priorityBadge.className = 'priority-badge';
        if (data.severity_color === 'red') {
            priorityBadge.classList.add('high');
        } else if (data.severity_color === 'orange') {
            priorityBadge.classList.add('moderate');
        } else {
            priorityBadge.classList.add('none');
        }
    }

    const timeframeEl = document.getElementById('timeframeText');
    if (timeframeEl) timeframeEl.textContent = data.timeframe;

    const recCard = document.getElementById('recommendationCard');
    if (recCard && isHealthy) {
        recCard.style.background = '#edf9f2';
        recCard.style.borderColor = '#a8e6c3';
    }
}

function downloadReport() {
    if (!lastDiagnosisData) return;
    const d = lastDiagnosisData;
    const lines = [
        'PLANT CARE NET — DIAGNOSIS REPORT',
        '='.repeat(40),
        `Date: ${new Date().toLocaleString()}`,
        '',
        'DIAGNOSIS RESULTS',
        '-'.repeat(40),
        `Condition Detected : ${d.disease}`,
        `Confidence Score   : ${d.confidence}%`,
        '',
    ];
    if (!d.is_healthy) {
        lines.push(
            'SEVERITY ANALYSIS',
            '-'.repeat(40),
            `Infected Area      : ${d.severity_percentage}%`,
            `Severity Level     : ${d.severity_level}`,
            ''
        );
    }
    lines.push(
        'TREATMENT RECOMMENDATION',
        '-'.repeat(40),
        `Priority           : ${d.priority}`,
        `Timeframe          : ${d.timeframe}`,
        `Recommendation     : ${d.treatment}`,
        '',
        '='.repeat(40),
        'Generated by Plant Care Net AI Platform',
        'Built with TensorFlow, OpenCV & Flask'
    );

    const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `PlantCareNet_Report_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}


// ===== RESEARCHER PORTAL =====

async function analyzeNutrient() {
    const fields = {
        N: document.getElementById('inputN'),
        P: document.getElementById('inputP'),
        K: document.getElementById('inputK'),
        temperature: document.getElementById('inputTemperature'),
        humidity: document.getElementById('inputHumidity'),
        ph: document.getElementById('inputPh')
    };

    for (const [key, el] of Object.entries(fields)) {
        if (!el || el.value === '') {
            alert(`Please fill in the ${key} field.`);
            if (el) el.focus();
            return;
        }
    }

    const payload = {};
    for (const [key, el] of Object.entries(fields)) {
        payload[key] = parseFloat(el.value);
    }

    const resultsSection = document.getElementById('nutrientResultsSection');
    const loadingCard = document.getElementById('nutrientLoadingCard');
    const resultsCard = document.getElementById('nutrientResultsCard');
    const errorCard = document.getElementById('nutrientErrorCard');

    resultsSection.style.display = 'block';
    loadingCard.style.display = 'block';
    resultsCard.style.display = 'none';
    errorCard.style.display = 'none';

    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        const response = await fetch('/predict/nutrient', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        loadingCard.style.display = 'none';

        if (data.success) {
            renderNutrientResults(data, payload);
            resultsCard.style.display = 'block';
        } else {
            document.getElementById('nutrientErrorText').textContent =
                data.error || 'Analysis failed.';
            errorCard.style.display = 'block';
        }

    } catch (err) {
        loadingCard.style.display = 'none';
        document.getElementById('nutrientErrorText').textContent =
            'Network error. Please try again.';
        errorCard.style.display = 'block';
    }
}

function renderNutrientResults(data, payload) {
    const statusEl = document.getElementById('nutrientResult');
    if (statusEl) statusEl.textContent = data.nutrient_status;

    const confEl = document.getElementById('nutrientConfidenceResult');
    if (confEl) confEl.textContent = data.confidence + '%';

    // All class probabilities
    const probContainer = document.getElementById('nutrientAllProbabilities');
    if (probContainer && data.all_probabilities) {
        probContainer.innerHTML = data.all_probabilities.map(item => `
            <div style="margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;
                            font-size:0.78rem;margin-bottom:3px">
                    <span style="color:var(--gray-800);font-weight:500">
                        ${item.label}
                    </span>
                    <span style="color:var(--gray-600)">${item.probability}%</span>
                </div>
                <div style="height:6px;background:var(--gray-200);
                            border-radius:50px;overflow:hidden">
                    <div style="height:100%;width:${item.probability}%;
                                background:${item.probability > 50 ?
                                    'var(--blue-600)' : 'var(--gray-400)'};
                                border-radius:50px;transition:width 0.8s ease">
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Input summary
    const summaryFields = {
        sumN: payload.N + ' kg/ha',
        sumP: payload.P + ' kg/ha',
        sumK: payload.K + ' kg/ha',
        sumTemp: payload.temperature + ' °C',
        sumHumidity: payload.humidity + '%',
        sumPh: payload.ph
    };
    for (const [id, val] of Object.entries(summaryFields)) {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    }

    // SHAP Chart
    const shapSection = document.getElementById('shapSection');
    const shapImage = document.getElementById('shapImage');
    if (shapSection && shapImage && data.shap_chart) {
        shapImage.src = data.shap_chart;
        shapSection.style.display = 'block';
    }

    // Recommendation
    const treatEl = document.getElementById('nutrientTreatmentText');
    if (treatEl) treatEl.textContent = data.treatment;

    const priorityBadge = document.getElementById('nutrientPriorityBadge');
    if (priorityBadge) {
        priorityBadge.textContent = data.priority;
        priorityBadge.className = 'priority-badge';
        if (data.severity_color === 'red') {
            priorityBadge.classList.add('high');
        } else if (data.severity_color === 'orange') {
            priorityBadge.classList.add('moderate');
        } else {
            priorityBadge.classList.add('none');
        }
    }

    const timeEl = document.getElementById('nutrientTimeframeText');
    if (timeEl) timeEl.textContent = data.timeframe;
}

function resetNutrient() {
    const rs = document.getElementById('nutrientResultsSection');
    if (rs) rs.style.display = 'none';
    ['inputN', 'inputP', 'inputK',
     'inputTemperature', 'inputHumidity', 'inputPh'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
}