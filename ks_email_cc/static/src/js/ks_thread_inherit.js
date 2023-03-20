/** @odoo-module **/

import { registerClassPatchModel,registerInstancePatchModel } from '@mail/model/model_core';

registerClassPatchModel('mail.thread', 'ks_email_cc/static/src/js/thread_inherit.js', {
   performRpcMessagePost({ postData, threadId, threadModel }) {
        if(Object.keys(postData).includes('subtype_xmlid') && postData['subtype_xmlid'] == 'mail.mt_comment'){
            if(Object.keys(postData).includes('context')){
                postData.context.ks_from_button = true
            } else{
                postData['context'] = {'ks_from_button': true}
            }
        }

        return this.env.services.rpc({
            model: threadModel,
            method: 'message_post',
            args: [threadId],
            kwargs: postData,
        });
    }
});

