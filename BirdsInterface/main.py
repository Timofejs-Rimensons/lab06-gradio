import gradio as gr
from Services.BirdsApiService import BirdsApiService
from datetime import datetime

svc = BirdsApiService()


def get_bird_choices():
    birds_df = svc.get_birds()
    return [(f"{row['nickname']} [{row['ring_code']}]", row['id']) for _, row in birds_df.iterrows()]

def get_species_choices():
    species_df = svc.get_species()
    return [(f"{row['name']} [{row['scientific_name']}]", row['id']) for _, row in species_df.iterrows()]

def load_species(status_filter):
    df = svc.get_species()
    if status_filter and status_filter != "All":
        df = df[df["conservation_status"] == status_filter]
    return df

def create_species(name, scientific_name, family, conservation_status, wingspan_cm):
    svc.add_species(name, scientific_name, family, conservation_status, float(wingspan_cm))
    return svc.get_species()

def load_birds():
    return svc.get_birds()

def refresh_species_dropdown():
    return gr.Dropdown(choices=get_species_choices())

def create_bird(nickname, ring_code, age, species_id):
    svc.add_birds(int(species_id), nickname, ring_code, int(age))
    return svc.get_birds()

def load_sightings(observer_filter):
    df = svc.get_bird_spotting()
    if observer_filter and observer_filter.strip():
        df = df[df["observer_name"].str.contains(observer_filter, case=False, na=False)]
    return df

def refresh_bird_dropdown():
    return gr.Dropdown(choices=get_bird_choices())

def create_sighting(bird_id, spotted_at_str, location, observer_name, notes):
    spotted_at = datetime.fromisoformat(spotted_at_str)
    svc.add_bird_spotting(int(bird_id), spotted_at, location, observer_name, notes or None)
    return svc.get_bird_spotting()


STATUS_CHOICES = [
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]

with gr.Blocks(title="Birds Viewer") as demo:
    gr.Markdown("## Birds Viewer")
    gr.Markdown("Live data from the Birds API at `http://127.0.0.1:8000`")

    with gr.Tabs():

        with gr.TabItem("Species"):
            with gr.Row():
                species_status_filter = gr.Dropdown(
                    choices=STATUS_CHOICES, value="All",
                    label="Filter by conservation status", scale=3
                )
                species_refresh_btn = gr.Button("Refresh", scale=1)

            species_table = gr.DataFrame(
                value=svc.get_species(),
                label="Species",
                interactive=False
            )

            with gr.Accordion("+ Add new species", open=False):
                with gr.Row():
                    sp_name       = gr.Textbox(label="Name", placeholder="e.g. Atlantic Puffin")
                    sp_sci_name   = gr.Textbox(label="Scientific name", placeholder="e.g. Fratercula arctica")
                with gr.Row():
                    sp_family     = gr.Textbox(label="Family", placeholder="e.g. Alcidae")
                    sp_status     = gr.Dropdown(choices=STATUS_CHOICES[1:], value="LC", label="Conservation status")
                    sp_wingspan   = gr.Slider(0, 300, value=55, label="Wingspan (cm)")
                sp_create_btn = gr.Button("Create species", variant="primary")

        with gr.TabItem("Birds"):
            birds_refresh_btn = gr.Button("Refresh")

            birds_table = gr.DataFrame(
                value=svc.get_birds(),
                label="Birds",
                interactive=False
            )

            with gr.Accordion("+ Add new bird", open=False):
                with gr.Row():
                    b_nickname  = gr.Textbox(label="Nickname", placeholder="e.g. Skipper")
                    b_ring_code = gr.Textbox(label="Ring code", placeholder="e.g. NR-1234")
                with gr.Row():
                    b_age       = gr.Number(label="Age (years)", value=0, minimum=0)
                    b_species   = gr.Dropdown(
                        choices=get_species_choices(),
                        label="Species"
                    )
                with gr.Row():
                    b_refresh_species_btn = gr.Button("Refresh species list", scale=1)
                    b_create_btn          = gr.Button("Create bird", variant="primary", scale=2)

        with gr.TabItem("Sightings"):
            with gr.Row():
                sighting_observer_filter = gr.Textbox(
                    label="Filter by observer name",
                    placeholder="e.g. Jane",
                    scale=3
                )
                sightings_refresh_btn = gr.Button("Refresh", scale=1)

            sightings_table = gr.DataFrame(
                value=svc.get_bird_spotting(),
                label="Sightings",
                interactive=False
            )

            with gr.Accordion("+ Add new sighting", open=False):
                with gr.Row():
                    s_bird = gr.Dropdown(
                        choices=get_bird_choices(),
                        label="Bird"
                    )
                    s_refresh_birds_btn = gr.Button("Refresh bird list", scale=1)
                with gr.Row():
                    s_spotted_at    = gr.Textbox(label="Spotted at (ISO 8601)", placeholder="e.g. 2024-06-01T09:30:00")
                    s_location      = gr.Textbox(label="Location", placeholder="e.g. Cliffs of Moher")
                with gr.Row():
                    s_observer_name = gr.Textbox(label="Observer name", placeholder="e.g. Jane Doe")
                    s_notes         = gr.Textbox(label="Notes (optional)", placeholder="e.g. Flying low over the water")
                s_create_btn = gr.Button("Create sighting", variant="primary")

    species_status_filter.change(fn=load_species, inputs=species_status_filter, outputs=species_table)
    species_refresh_btn.click(fn=load_species, inputs=species_status_filter, outputs=species_table)
    sp_create_btn.click(
        fn=create_species,
        inputs=[sp_name, sp_sci_name, sp_family, sp_status, sp_wingspan],
        outputs=species_table
    )

    birds_refresh_btn.click(fn=load_birds, outputs=birds_table)
    b_refresh_species_btn.click(fn=refresh_species_dropdown, outputs=b_species)
    b_create_btn.click(
        fn=create_bird,
        inputs=[b_nickname, b_ring_code, b_age, b_species],
        outputs=birds_table
    )

    sighting_observer_filter.change(fn=load_sightings, inputs=sighting_observer_filter, outputs=sightings_table)
    sightings_refresh_btn.click(fn=load_sightings, inputs=sighting_observer_filter, outputs=sightings_table)
    s_refresh_birds_btn.click(fn=refresh_bird_dropdown, outputs=s_bird)
    s_create_btn.click(
        fn=create_sighting,
        inputs=[s_bird, s_spotted_at, s_location, s_observer_name, s_notes],
        outputs=sightings_table
    )

if __name__ == "__main__":
    demo.launch()