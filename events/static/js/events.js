/**
 * Created by rkessler on 2016-12-03.
 */

function update_event_participation_status(event_id, new_state, success_callback){
    $.ajax({
        method: 'POST',
        url: get_url('event_pstatus'),
        data: {
            event_id: event_id,
            new_state: new_state,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            success_callback()
        }
    });
}