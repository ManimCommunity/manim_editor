import { send_json, flash } from "./utils";

function set_scene_status(scene: HTMLTableRowElement, status: boolean): void {
    let scene_check_box = scene.getElementsByClassName("scene-check-box")[0] as HTMLInputElement;
    scene_check_box.checked = status;
    // apply to all sections
    let section_check_boxes = scene.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    for (let section of section_check_boxes)
        section.checked = status;
}

// check if entire scene got turned on or off
function update_scene(scene: HTMLTableRowElement): void {
    let section_check_boxes = scene.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    let new_status = section_check_boxes[0].checked;
    // check if all sections have same status
    for (let i = 1; i < section_check_boxes.length; ++i)
        if (section_check_boxes[i].checked != new_status)
            return;
    set_scene_status(scene, new_status);
}

// activate button when at least one section is selected
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

// set click callbacks for scenes and sections
function watch_indices(): void {
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
    let used_priorities: boolean[] = Array(scene_priorities.length).fill(false);
    for (let i = 0; i < scene_priorities.length; ++i) {
        let priority = parseInt(scene_priorities[i].value);
        if (used_priorities[priority]) {
            flash(`The priority ${priority} can't be used twice.`, "danger");
            return [];
        }
        used_priorities[priority] = true;
        priorities.push(priority);
    }
    return priorities;
}

// return list of sections in order of priority of scenes
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
    // log debug
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

function set_button(): void {
    let button = document.getElementById("confirm-button") as HTMLButtonElement;
    button.addEventListener("click", () => {
        let selected_sections = get_selected_sections();
        if (selected_sections.length) {
            let payload = {
                "name": button.dataset.project_name as string,
                "sections": selected_sections,
            };
            send_json(button.dataset.target as string, payload, (response: any) => {
                console.log(response);
            });
        }
    });
}

document.body.onload = () => {
    watch_indices();
    set_button();
};
