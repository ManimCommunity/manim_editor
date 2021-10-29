import { send_json, flash, spin_button } from "./utils";

// check or uncheck all sections in scene
function set_scene_status(scene: HTMLTableRowElement, status: boolean): void {
    let scene_check_box = scene.getElementsByClassName("scene-check-box")[0] as HTMLInputElement;
    scene_check_box.checked = status;
    // apply to all sections
    let section_check_boxes = scene.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    for (let section of section_check_boxes)
        section.checked = status;
}

// check if entire scene got turned on or off and update scene status accordingly
function update_scene(scene: HTMLTableRowElement): void {
    let section_check_boxes = scene.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    let new_status = section_check_boxes[0].checked;
    // check if all sections have same status
    for (let i = 1; i < section_check_boxes.length; ++i)
        if (section_check_boxes[i].checked != new_status)
            return;
    set_scene_status(scene, new_status);
}

// set click callbacks for scenes and sections
function watch_check_boxes(): void {
    // scenes
    let scenes = document.getElementsByClassName("scene-select") as HTMLCollectionOf<HTMLTableRowElement>;
    for (let scene of scenes) {
        let scene_check_box = scene.getElementsByClassName("scene-check-box")[0] as HTMLInputElement;
        scene_check_box.addEventListener("click", () => {
            set_scene_status(scene, scene_check_box.checked);
            update_button();
        });
        // sections
        let sections = scene.getElementsByClassName("section-select") as HTMLCollectionOf<HTMLTableRowElement>;
        for (let section of sections) {
            let section_check_box = section.getElementsByClassName("section-check-box")[0] as HTMLInputElement;
            section_check_box.addEventListener("click", () => {
                update_scene(scene);
                update_button();
            })
        }
    }
}

// activate button when at least one section is selected
// has to be executed every time the selections get clicked
function update_button(): void {
    let section_check_boxes = document.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    let button = document.getElementById("confirm-button") as HTMLButtonElement;
    for (let section_check_box of section_check_boxes) {
        if (section_check_box.checked) {
            button.disabled = false;
            return;
        }
    }
    button.disabled = true;
}

type Section = {
    scene_id: number;
    section_id: number;
}

// return list containing at index i the priority of the scene with priority i
// return empty list if priority used twice
function get_scene_priorities(): number[] {
    let scene_priorities = document.getElementsByClassName("scene-priority") as HTMLCollectionOf<HTMLSelectElement>;
    let priorities: number[] = [];
    // used to check if priority is used twice
    let used: boolean[] = Array(scene_priorities.length).fill(false);
    for (let i = 0; i < scene_priorities.length; ++i) {
        let priority = parseInt(scene_priorities[i].value);
        if (used[priority]) {
            flash(`The priority ${priority} can't be used twice.`, "danger");
            return [];
        }
        used[priority] = true;
        priorities.push(priority);
    }
    return priorities;
}

// return list of selected sections in order of priority of scenes
function get_selected_sections(): Section[] {
    // used as lookup table
    let priorities = get_scene_priorities();
    if (!priorities.length)
        return [];

    let scenes = document.getElementsByClassName("scene-select") as HTMLCollectionOf<HTMLTableRowElement>;
    // list of selected sections for each scene in order of priority
    let selected_scene_sections: Section[][] = [];
    for (let i = 0; i < scenes.length; ++i)
        selected_scene_sections.push([]);
    // go through scenes
    for (let i = 0; i < scenes.length; ++i) {
        let section_check_boxes = scenes[i].getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
        // go through selected check boxes in this scene
        for (let section_check_box of section_check_boxes)
            if (section_check_box.checked) {
                // resolve priority
                selected_scene_sections[priorities[i]].push({
                    "scene_id": i,
                    "section_id": parseInt(section_check_box.dataset.section_id as string),
                });
            }
    }
    let sections: Section[] = [];
    for (let i = 0; i < scenes.length; ++i) {
        for (let section of selected_scene_sections[i])
            sections.push(section);
    }
    // log order of scenes used
    let last_scene_id = -1;
    let scene_log = "Used scene order: ";
    for (let section of sections) {
        if (section.scene_id != last_scene_id) {
            scene_log += `${section.scene_id} `;
            last_scene_id = section.scene_id;
        }
    }
    console.log(scene_log);
    return sections;
}

function watch_button(): void {
    let button = document.getElementById("confirm-button") as HTMLButtonElement;
    let target = button.dataset.target as string;
    let project_name = button.dataset.project_name as string;
    let success_url = button.dataset.success_url as string;
    button.addEventListener("click", () => {
        let selected_sections = get_selected_sections();
        // show flashes
        window.scrollTo(0, 0);
        // selection valid?
        if (selected_sections.length) {
            flash("The project is being populated, this might take a few minutes. Open the terminal for more info.", "info");
            spin_button(button);
            let payload = {
                "name": project_name,
                "sections": selected_sections,
            };
            send_json(target as string, payload, (response: any) => {
                // redirect at success
                if (response.success) {
                    window.location.href = success_url;
                }
                else
                    flash(`The editor unexpectedly failed to populate the project '${project_name}'. For more information see the console log. Please consider opening an Issue on GitHub if this problem persists.`, "danger");
            });
        }
    });
}

document.body.onload = () => {
    watch_check_boxes();
    watch_button();
    // first update is for when the browser remembered some selections but the button stays inactive
    update_button();
};
