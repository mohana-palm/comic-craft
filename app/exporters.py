import os
from datetime import datetime

from fpdf import FPDF


OUTPUT_DIR = "static/exports"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def clean_text(text):
    return (
        text
        .replace("—", "-")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
    )


def save_pdf(layout):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"comic_{timestamp}.pdf"

    filepath = os.path.join(
        OUTPUT_DIR,
        filename
    )

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Arial",
            "B",
            18
        )

        pdf.cell(
            0,
            12,
            clean_text(
                f"Panel {panel['panel_number']}: "
                f"{panel['title']}"
            ),
            ln=True
        )

        pdf.ln(5)

        image_path = panel["image"].replace(
            "/static/",
            "static/"
        )

        if os.path.exists(image_path):

            pdf.image(
                image_path,
                x=15,
                w=180
            )

        pdf.ln(8)

        pdf.set_font(
            "Arial",
            "I",
            11
        )

        pdf.multi_cell(
            0,
            7,
            clean_text(
                panel["scene_description"]
            )
        )

        pdf.ln(5)

        pdf.set_font(
            "Arial",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Caption: "
            + clean_text(
                panel["caption"]
            )
        )

        pdf.ln(3)

        pdf.set_font(
            "Arial",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Narration: "
            + clean_text(
                panel["narration"]
            )
        )

        pdf.ln(3)

        pdf.multi_cell(
            0,
            7,
            "Dialogue: "
            + clean_text(
                panel["dialogue"]
            )
        )

    pdf.output(filepath)

    return f"/static/exports/{filename}"