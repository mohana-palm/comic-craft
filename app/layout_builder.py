import json


def build_comic_layout(
    panels,
    story
):

    story_data = json.loads(story)

    story_by_panel = {}

    for item in story_data:

        story_by_panel[
            item["panel_number"]
        ] = item

    layout = []

    for panel in panels:

        number = panel["panel_number"]

        story_info = story_by_panel.get(
            number,
            {}
        )

        layout.append({

            "panel_number": number,

            "title": panel["title"],

            "scene_description":
                panel["scene_description"],

            "image":
                panel["image"],

            "narration":
                story_info.get(
                    "narration",
                    ""
                ),

            "caption":
                story_info.get(
                    "caption",
                    ""
                ),

            "dialogue":
                story_info.get(
                    "dialogue",
                    ""
                )
        })

    return layout