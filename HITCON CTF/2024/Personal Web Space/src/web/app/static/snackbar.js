const ts = (selector) => {
    return {
        snackbar: ({ content }) => {
            let snackbar = dqs(selector);

            if (!snackbar.dataset.listener) {
                snackbar.on("animationend", (ev) => {
                    ev.target.classList.remove("active");
                });
                snackbar.dataset.listener = true;
            }

            snackbar.dqs(".content").innerText = content;

            // reset animation
            snackbar.classList.toggle("active", false);

            // reflow magic
            void snackbar.offsetWidth;

            snackbar.classList.add("active");
        }
    }
}