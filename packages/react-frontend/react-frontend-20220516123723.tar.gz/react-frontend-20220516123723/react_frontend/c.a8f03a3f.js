import{d as t,_ as e,s,e as i,m as a,$ as n,f as o,ar as r,n as d}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";import"./c.e38196bb.js";import"./c.027db416.js";import"./c.8cbd7110.js";e([d("more-info-person")],(function(e,s){return{F:class extends s{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"stateObj",value:void 0},{kind:"field",key:"_entityArray",value:()=>a((t=>[t]))},{kind:"method",key:"render",value:function(){var t;return this.hass&&this.stateObj?n`
      ${this.stateObj.attributes.latitude&&this.stateObj.attributes.longitude?n`
            <ha-map
              .hass=${this.hass}
              .entities=${this._entityArray(this.stateObj.entity_id)}
              autoFit
            ></ha-map>
          `:""}
      ${null!==(t=this.hass.user)&&void 0!==t&&t.is_admin&&"not_home"===this.stateObj.state&&this.stateObj.attributes.latitude&&this.stateObj.attributes.longitude?n`
            <div class="actions">
              <mwc-button @click=${this._handleAction}>
                ${this.hass.localize("ui.dialogs.more_info_control.person.create_zone")}
              </mwc-button>
            </div>
          `:""}
      <ha-attributes
        .hass=${this.hass}
        .stateObj=${this.stateObj}
        extra-filters="id,user_id,editable"
      ></ha-attributes>
    `:n``}},{kind:"method",key:"_handleAction",value:function(){this.stateObj.attributes.latitude,this.stateObj.attributes.longitude,t("/config/zone/new"),o(this,"hass-more-info",{entityId:null})}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      .flex {
        display: flex;
        justify-content: space-between;
      }
      .actions {
        margin: 8px 0;
        text-align: right;
      }
      ha-map {
        margin-top: 16px;
        margin-bottom: 16px;
      }
    `}}]}}),s);
