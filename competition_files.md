# RSNA Knee Abnormality Detection — official file inventory

Source: [Kaggle competition data page](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/data)

The complete competition input is approximately **569.76 GB** and contains about **819,640 files**. It is not practical to copy the complete MRI archive into this chat workspace. Attach the competition directly to a Kaggle Notebook for training and inference.

```text
rsna-knee-abnormality-detection/
├── train.csv
├── train_series.csv
├── train_series/
│   └── <StudyInstanceUID>/
│       └── <SeriesInstanceUID>/
│           └── <SOPInstanceUID>.dcm
├── test.csv
├── test_series.csv
├── test_series/
│   └── <StudyInstanceUID>/
│       └── <SeriesInstanceUID>/
│           └── <SOPInstanceUID>.dcm
└── sample_submission.csv
```

## File meanings

### `train.csv`

One row per training study. It contains `StudyInstanceUID`, the free-text `Report`, and the twelve binary target columns when structured labels are available:

```text
StudyInstanceUID
Report
ACL
MCL
Medial Meniscus
Lateral Meniscus
Medial OA
Lateral OA
PF OA
Effusion
Synovitis
Baker's
Contusion
Fracture
```

The report can be multilingual. Structured labels are missing for many studies; missing is not the same as negative.

### `train_series.csv`

One row per training MRI series:

```text
StudyInstanceUID
SeriesInstanceUID
Fluid_Sensitive
Fat_Suppression
Anatomical_Plane
```

Each row points to a directory under `train_series/<StudyInstanceUID>/<SeriesInstanceUID>/`.

### `train_series/`

Training DICOM image slices. Each `.dcm` file is one image slice. A series usually contains about 20–45 slices, with a long tail. The official data page notes mixed DICOM transfer syntaxes, so decoding support must be tested in Kaggle.

### `test.csv`

Example test study IDs. During scoring, Kaggle replaces the example test data with the hidden test data. The report is not provided for test studies.

### `test_series.csv`

Series descriptors for the example test studies, with the same columns as `train_series.csv`. Kaggle replaces these descriptors during scoring.

### `test_series/`

Example test DICOM slices. Kaggle replaces them during scoring.

### `sample_submission.csv`

Submission template with `StudyInstanceUID` and the twelve target columns. The sample values are set to `0.5`.

## Kaggle input path

Inside a Kaggle Notebook, the attached competition is normally available under a path similar to:

```text
/kaggle/input/rsna-knee-abnormality-detection/
```

Do not hardcode that name without checking the Input panel. Use this compact discovery cell:

```python
from pathlib import Path

roots = [
    p.parent for p in Path('/kaggle/input').glob('*/train.csv')
    if (p.parent / 'sample_submission.csv').is_file()
]
assert len(roots) == 1, f'Expected one competition input, found: {roots}'
DATA = roots[0]
print(DATA)
```

Then read the small metadata files:

```python
import pandas as pd

train = pd.read_csv(DATA / 'train.csv')
train_series = pd.read_csv(DATA / 'train_series.csv')
test = pd.read_csv(DATA / 'test.csv')
test_series = pd.read_csv(DATA / 'test_series.csv')
sample = pd.read_csv(DATA / 'sample_submission.csv')

for name, frame in {
    'train': train,
    'train_series': train_series,
    'test': test,
    'test_series': test_series,
    'sample_submission': sample,
}.items():
    print(name, frame.shape, frame.columns.tolist())
```

The MRI data should stay attached to Kaggle. Downloading all DICOMs to a local computer is unnecessary for a Code Competition submission and may require hundreds of gigabytes of storage.

