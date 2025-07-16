const data2 = document.currentScript.dataset;
const dashboard_integration_id = data2.dashboardintegrationid;
const superset_domain = data2.supersetdomain;
let iframe_height = data2.iframeheight;

// Display dashboard inside #graph element
supersetEmbeddedSdk.embedDashboard({
    id: dashboard_integration_id,
    supersetDomain: "https://" + superset_domain,
    mountPoint: document.getElementById("superset-integration"),
    fetchGuestToken: () => fetchGuestTokenFromBackend(),
    dashboardUiConfig: {
        hideTitle: true,
        filters: {
            expanded: true,
        }
    },
});

let iframe = document.getElementById("superset-integration").firstElementChild;

if (typeof iframe_height === 'undefined') {
    iframe_height = "1200px";  // If no iframe_height set, we set iframe_height
} else if (!isNaN(iframe_height)) {
    iframe_height = iframe_height + "px";  // If iframe_height is a number, we add "px" at the end
}

window.onload = (event) => {
    iframe.height = iframe_height;
};

const btn_fullscreen = document.getElementById("superset-fullscreen");
const btn_fullscreen_exit = document.getElementById("superset-fullscreen-exit");
const header = document.getElementsByTagName("header")[0];
const footer = document.getElementsByTagName("footer")[0];
let superset_integration = document.getElementById("superset-integration");
btn_fullscreen.addEventListener("click", function()
{
    try {
        header.style.display = "none";
    } catch (error) {
        // no header element
    }

    try {
        footer.style.display = "none";
    } catch (error) {
        // no footer element
    }
    
    btn_fullscreen_exit.style.display = "block";
    btn_fullscreen_exit.style.visibility = "visible";
    btn_fullscreen_exit.style.opacity = 100;
    superset_integration.classList.add("fullScreen");
    iframe.height = "100%";
}); 


btn_fullscreen_exit.addEventListener("click", function()
{ 
    try {
        header.style.display = "block";
    } catch (error) {
        // no header element
    }

    try {
        footer.style.display = "block";
    } catch (error) {
        // no footer element
    }

    btn_fullscreen_exit.style.display = "none";
    superset_integration.classList.remove("fullScreen");
    iframe.height = iframe_height;
});
