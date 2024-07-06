    /** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment } from "@web/core/utils/render";
export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
console.log('j2working......')
var Dynamic = publicWidget.Widget.extend({
    	selector: '.event_snippet_blog',
    	willStart: async function() {
    	    const data = await jsonrpc('/latest_events',
        	).then((data) => {
            	this.data = data;
        	});
    	},
    	start: function() {
    	console.log("function worked")
        	var chunks = chunk(this.data,4)
        	chunks[0].is_active = true
        	var carousel_id = "id" + Math.random().toString(8).slice(2);
        	this.$el.find('#courosel').html(renderToFragment('school_management.events_snippet_carousel', {
        	    'chunks':chunks,
        	    'carousel_id': carousel_id
            	})
        	)
    	},
	});
	publicWidget.registry.event_snippet_blog = Dynamic;
	return Dynamic;