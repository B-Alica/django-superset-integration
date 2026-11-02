const data2 = document.currentScript.dataset;
const dashboard_integration_id = data2.dashboardintegrationid;
const superset_domain = data2.supersetdomain;
let iframe_height = data2.iframeheight;

// Display dashboard inside #graph element
const dashboard = supersetEmbeddedSdk.embedDashboard({
    id: dashboard_integration_id,
    supersetDomain: "https://" + superset_domain,
    mountPoint: document.getElementById("superset-integration"),
    fetchGuestToken: () => fetchGuestTokenFromBackend(),
    dashboardUiConfig: {
        hideTitle: true,
        filters: {
            expanded: true,
        },
        emitDataMasks: true // Emit filter state changes
    },
    iframeSandboxExtras: ['allow-top-navigation-by-user-activation', 'allow-popups-to-escape-sandbox']
});

function processDataMaskChange(dataMaskConfig) {
    console.log("Received a data mask change from the dashboard:");
    console.log(dataMaskConfig);
}

dashboard.then(dashboardElement => {
    dashboardElement.observeDataMask(processDataMaskChange);
});

// const response = await fetch(
//   "https://"+superset_domain+"/api/v1/dashboard/"+dashboard_integration_id+"/permalink",
//   {
//     method: "POST",
//     headers: {
//       "Authorization": `Bearer ${accessToken}`,
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({ key: "value" })
//   }
// );
// const data = await response.json();
// console.log(data);


let iframe = document.getElementById("superset-integration").firstElementChild;

if (typeof iframe_height === 'undefined') {
    iframe_height = "1200px";  // If no iframe_height set, we set iframe_height
} else if (!isNaN(iframe_height)) {
    iframe_height = iframe_height + "px";  // If iframe_height is a number, we add "px" at the end
}

window.onload = (event) => {
    iframe.height = iframe_height;
    // Ajouter les attributs allow-popups-to-escape-sandbox et allow-top-navigation-by-user-activation à l'iframe
    iframe.sandbox.add("allow-popups-to-escape-sandbox");
    iframe.sandbox.add("allow-top-navigation-by-user-activation");
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


//exit fullscreen
function exit_fullscreen(){
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
}


btn_fullscreen_exit.addEventListener("click", function()
{ 
    exit_fullscreen();
});

$(document).on( "keyup", function(e) {
    if (e.key === "Escape") {
        exit_fullscreen();
    }
});
