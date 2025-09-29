// Get guest token from django app backend
// The token has a lifetime of 5 min. This function is called
// periodically to refresh the token

const data = document.currentScript.dataset;
const dashboard_id = data.dashboardid;
let fetch_url = '/superset_integration/guest_token/' + dashboard_id;

async function fetchGuestTokenFromBackend() {
    const response = await fetch(fetch_url);
    const token = await response.text();
    return token;
}
