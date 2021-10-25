export function select_file(id: string): void {
    let selector = document.getElementById(id) as HTMLInputElement;
    selector.addEventListener("change", (file) => {
        console.log(file);
    });
}

// send json via POST and parse json resonse
export function send_json(url: string, payload: any, callback: { (response: any): void; }): void {
    let request = new XMLHttpRequest();
    request.onload = () => {
        if (request.status == 200)
            // if (request.responseType != "json")
            //     console.error(`Failed POST to '${url}' with type ${request.responseType}.`);
            // else
            callback(JSON.parse(request.responseText));
        else
            console.error(`Failed POST to '${url}' with status ${request.status}.`);
    };
    request.onerror = () => {
        console.error(`Failed to POST to '${url}'.`);
    };
    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(payload));
}

// download file and parse json
export function get_json(url: string, callback: { (response: any): void; }): void {
    let request = new XMLHttpRequest();
    request.onload = () => {
        if (request.status == 200)
            // if (request.responseType != "json")
            //     console.error(`Failed to load json '${url}' with type ${request.responseType}.`);
            // else
            callback(JSON.parse(request.responseText));
        else
            console.error(`Failed to load json '${url}' with status ${request.status}`);
    };
    request.onerror = () => {
        console.error(`Failed to load json '${url}'`);
    };
    request.open("GET", url, true);
    request.send();
}

export function flash(message: string, category: string): void {
    let flashes = document.getElementById("flashes") as HTMLDivElement;
    let wrapper = document.createElement("div");
    flashes.appendChild(wrapper);
    wrapper.innerHTML =
        `<div class="alert alert-${category} alert-dismissible fade show mt-3" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
         </div>`

}

// add loading spinner to button
// deletes innerText of button -> can't be undone
export function spin_button(button: HTMLButtonElement): void {
    button.disabled = true;
    button.innerText = "";
    let spinner = document.createElement("div");
    button.appendChild(spinner);
    spinner.innerHTML =
        `<div>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Loading...
        </div>`;
}
