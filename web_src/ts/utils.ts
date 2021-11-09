// send json via POST and parse json response
// optional onfailure callback
export function send_json(url: string,
    payload: any,
    onsuccess: { (response: any): void; },
    onfailure: { (): void } = () => { }): void {
    let request = new XMLHttpRequest();
    request.onload = () => {
        if (request.status == 200)
            onsuccess(JSON.parse(request.responseText));
        else {
            console.error(`Failed POST to '${url}' with status ${request.status}.`);
            onfailure();
        }
    };
    request.onerror = () => {
        console.error(`Failed to POST to '${url}'.`);
        onfailure();
    };
    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(payload));
}

// download file and parse json
export function get_json(url: string,
    callback: { (response: any): void; },
    onfailure: { (): void } = () => { }): void {
    let request = new XMLHttpRequest();
    request.onload = () => {
        if (request.status == 200)
            callback(JSON.parse(request.responseText));
        else {
            console.error(`Failed to load json '${url}' with status ${request.status}`);
            onfailure();
        }
    };
    request.onerror = () => {
        console.error(`Failed to load json '${url}'`);
        onfailure();
    };
    request.open("GET", url, true);
    request.send();
}

// front end implementation of flasks flash function
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
