"""Compact Kaggle notebook cell for locating and checking competition files."""

from pathlib import Path
import pandas as pd

roots = [
    p.parent for p in Path('/kaggle/input').glob('*/train.csv')
    if (p.parent / 'sample_submission.csv').is_file()
]
assert len(roots) == 1, f'Expected one competition input, found: {roots}'
data = roots[0]

expected = [
    'train.csv', 'train_series.csv', 'test.csv',
    'test_series.csv', 'sample_submission.csv',
    'train_series', 'test_series',
]
for name in expected:
    assert (data / name).exists(), f'Missing: {data / name}'

sample = pd.read_csv(data / 'sample_submission.csv')
train = pd.read_csv(data / 'train.csv')
assert sample.columns[0] == 'StudyInstanceUID'
targets = sample.columns[1:].tolist()
assert len(targets) == 12, targets
assert 'StudyInstanceUID' in train.columns

print('Competition input:', data)
print('train.csv:', train.shape)
print('Targets:', targets)
print('All expected top-level files/folders are present.')
