# pylint: disable=unused-argument, disable=super-init-not-called, no-self-use
from typing import Optional
import numpy as np
import numpy.typing as npt
from PIL import Image
from mandelia.model.manager import ProgressHandler

from mandelia.view.export import DataExport


class ModuloColoration:
    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        ...

    def to_bytes(self) -> bytes:
        ...

    def from_bytes(self, data: bytes) -> None:
        ...

    def bytes_size(self) -> int:
        ...

    def colorize(
        self, np_fractale: npt.NDArray[np.uint32]
    ) -> npt.NDArray[np.uint8]:
        ...


class Fractale:
    real: float
    imaginary: float
    pixel_size: float
    width: int
    height: int
    iterations: int
    need_update: bool

    def __init__(self, color: ModuloColoration, real: float = 0,
                 imaginary: float = 0, iterations: int = 1_000,
                 width: int = 128, height: int = 128, pixel_size: float = 0.02
                 ) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def __copy__(self) -> 'Fractale':
        ...

    def set_real(self, real: float) -> None:
        ...

    def set_imaginary(self, imaginary: float) -> None:
        ...

    def set_iterations(self, iterations: int) -> None:
        ...

    def resize(self, width: int, height: int) -> None:
        ...

    def iterations_sum(self) -> int:
        ...

    def iterations_per_pixel(self) -> int:
        ...

    def image(self) -> Image.Image:
        ...

    def image_at_size(self, width: int, height: int) -> Image.Image:
        ...

    def top(self) -> None:
        ...

    def middle_zoom(self, multiplier: float) -> None:
        ...

    def zoom(self, x: int, y: int, multiplier: float) -> None:
        ...

    def reset(self) -> None:
        ...

    def real_at_x(self, x: int) -> float:
        ...

    def imaginary_at_y(self, y: int) -> float:
        ...

    def to_bytes(self) -> bytes:
        ...

    def from_bytes(self, data: bytes) -> None:
        ...

    def bytes_size(self) -> int:
        ...

    def drop(
        self,
        data: DataExport,
        handler_progress: Optional[ProgressHandler] = None
    ) -> None:
        ...


class Julia(Fractale):
    c_r: float
    c_i: float

    def __init__(self, color: ModuloColoration, real: float = 0,
                 imaginary: float = 0, iterations: int = 1_000,
                 width: int = 128, height: int = 128, pixel_size: float = 0.02
                 ) -> None:
        ...

    def set_c_r(self, c_r: float) -> None:
        ...

    def set_c_i(self, c_i: float) -> None:
        ...


class Mandelbrot(Fractale):
    ...
