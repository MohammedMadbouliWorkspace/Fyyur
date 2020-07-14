window.parseISOString = function parseISOString(s) {
    var b = s.split(/\D+/);
    return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

try {
    let txta = $('#seeking_description');
    if (
        location.pathname === '/venues/create' ||
        location.pathname.includes('/venues') &&
        location.pathname.includes("edit")
    ) {
        let sTCheckbox = $('#seeking_talent');
        sTCheckbox.change(
            (e) => {
                if (e.target.checked === true) {
                    txta.attr('disabled', false)
                } else {
                    txta.attr('disabled', true)
                }

            }
        )
        if(sTCheckbox.attr("checked")) {
            txta.attr('disabled', false)
        }
    } else if (
        location.pathname === '/artists/create' ||
        location.pathname.includes('/artists') &&
        location.pathname.includes("edit")
    ) {
        let sTCheckbox = $('#seeking_venue');
        sTCheckbox.change(
            (e) => {
                if (e.target.checked === true) {
                    txta.attr('disabled', false)
                } else {
                    txta.attr('disabled', true)
                }

            }
        )
        if(sTCheckbox.attr("checked")) {
            txta.attr('disabled', false)
        }
    }
} catch (e) {
}