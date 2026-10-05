from fastapi import (
    APIRouter,
    Request,
    Form
)

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates


from app.gemini_flash import generate_outline

from app.gemini_pro import generate_story

from app.image_generator import generate_image

from app.layout_builder import build_comic_layout

from app.exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate_comic(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    # Step 1
    outline = generate_outline(

        story_prompt,

        character_name,

        setting,

        tone,

        art_style
    )


    # Step 2
    story = generate_story(
        outline
    )


    # Step 3
    panels = []


    for panel in outline:

        image_path = generate_image(

            panel["image_prompt"],

            panel["panel_number"]
        )


        panels.append({

            "panel_number":
                panel["panel_number"],

            "title":
                panel["title"],

            "scene_description":
                panel["scene_description"],

            "image":
                image_path
        })


    # Step 4
    layout = build_comic_layout(

        panels,

        story
    )


    # Step 5
    pdf_path = save_pdf(
        layout
    )


    return templates.TemplateResponse(
    request=request,
    name="comic_preview.html",
    context={
        "layout": layout,
        "pdf_path": pdf_path
    }
)

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(
    request: Request
):

   return templates.TemplateResponse(
    request=request,
    name="export_success.html",
    context={}
)