# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import time
from pathlib import Path as path_t
from typing import Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import skimage.transform as trfm
import tifffile as tiff

from cell_tracking_BC.in_out.graphics.dbe.matplotlib.style import CellAnnotationStyle
from cell_tracking_BC.type.sequence import BoundingBoxSlices, sequence_t


def SaveSequenceAnnotations(
    sequence: sequence_t, folder: path_t, file: Union[str, path_t], /
) -> None:
    """"""
    figure, axes = pypl.subplots(facecolor="k")
    canvas = figure.canvas

    annotated = None
    for f_idx in range(sequence.length):
        if f_idx % 5 == 0:
            print(f"    Writing frame {f_idx} @ {time.ctime()}...")

        axes.clear()
        axes.set_axis_off()
        axes.set_facecolor("k")

        frame = sequence.cell_frames[f_idx]
        description = frame.Description(margins=(0, -50))
        # for contours in description["cell_contours"].values():
        #     axes.scatter(
        #         contours[1],
        #         contours[0],
        #         color=(0.0, 0.8, 0.8, 0.3),
        #     )
        for contours in description["cell_contours"].values():
            for contour in contours:
                axes.plot(
                    contour[:, 1],
                    contour[:, 0],
                    linestyle=":",
                    color=(0.0, 0.8, 0.8, 0.3),
                )

        description = sequence.DescriptionOfFrame(f_idx)
        for text, position in description["track_labels"]:
            additionals = CellAnnotationStyle(False, "\n" in text)
            axes.annotate(
                text,
                nmpy.flipud(position),
                ha="center",
                **additionals,
            )
        canvas.draw()

        content = nmpy.array(canvas.renderer.buffer_rgba())[:, :, :3]
        if annotated is None:
            annotated = nmpy.empty((*content.shape, sequence.length), dtype=nmpy.uint8)
        annotated[..., f_idx] = content

    row_slice, col_slice = BoundingBoxSlices(annotated)
    annotated = annotated[row_slice, col_slice, :, :]
    annotated = trfm.resize(
        annotated, (*sequence.shape, 3, sequence.length), preserve_range=True
    )
    annotated = annotated.astype(nmpy.uint8, copy=False)
    annotated = nmpy.moveaxis(annotated, (0, 1, 2, 3), (2, 3, 1, 0))
    annotated = annotated[:, nmpy.newaxis, :, :, :]

    tiff.imwrite(
        str(folder / file),
        annotated,
        photometric="rgb",
        compression="deflate",
        planarconfig="separate",
        metadata={"axes": "XYZCT"},
    )

    pypl.close(fig=figure)  # To prevent remaining caught in event loop
