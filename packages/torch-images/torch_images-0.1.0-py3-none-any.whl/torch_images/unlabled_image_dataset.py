import torch
import zipfile
from torch.utils.data import Dataset
from torchvision.io import read_image, decode_image
from dataclasses import dataclass, field, MISSING, replace
from typing import Optional, Callable
from pathlib import Path
import warnings
from copy import copy


@dataclass(eq=False, frozen=True)
class UnlabledImageDataset(Dataset):
    """
    From a directory path, returns tensor images rescaled between 0 and 1.
    Also accepts zip files.
    """

    dir_path: str
    transform: Optional[Callable] = None

    image_paths: list[Path] = field(default_factory=list)
    extensions: tuple[str, ...] = (".jpeg", ".jpg", ".png")

    def __post_init__(self):
        if len(self.image_paths) == 0:
            path = Path(self.dir_path)
            if path.is_file():
                assert path.suffix == ".zip"
                with zipfile.ZipFile(path) as file:
                    self.image_paths.extend(
                        [
                            Path(name)
                            for name in file.namelist()
                            if Path(name).suffix in self.extensions
                        ]
                    )
            else:
                self.image_paths.extend(
                    [
                        name
                        for name in path.rglob("*.*")
                        if name.suffix in self.extensions
                    ]
                )

            assert len(self.image_paths) > 0

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        if Path(self.dir_path).suffix == ".zip":
            with zipfile.ZipFile(self.dir_path) as file:
                path = self.image_paths[idx]
                data = file.read(str(path))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                image = (
                    decode_image(
                        torch.frombuffer(copy(data), dtype=torch.uint8).clone()
                    )
                    / 255
                )
            warnings.resetwarnings()
        else:
            path = str(self.image_paths[idx])
            image = read_image(path) / 255.0

        if self.transform:
            image = self.transform(image)

        image.path = path  # type: ignore

        return image

    def split(
        self, pattern: str
    ) -> tuple["UnlabledImageDataset", "UnlabledImageDataset"]:
        match, no_match = [], []

        for path in self.image_paths:
            (no_match, match)[path.match(pattern)].append(path)

        return replace(self, image_paths=match), replace(self, image_paths=no_match)
