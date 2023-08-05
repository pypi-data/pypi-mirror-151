import{_ as t,s as e,e as a,t as s,g as i,i as r,$ as o,ar as c}from"./main-ac83c92b.js";import{i as d,z as h}from"./c.027db416.js";import{C as n,S as l,f as m,u as f}from"./c.3e14cfd3.js";import"./c.c8193d47.js";import"./c.8cbd7110.js";import"./c.47fa9be3.js";let k=t(null,(function(t,e){class k extends e{constructor(...e){super(...e),t(this)}}return{F:k,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[s()],key:"_cameraPrefs",value:void 0},{kind:"field",decorators:[s()],key:"_attached",value:()=>!1},{kind:"method",key:"connectedCallback",value:function(){i(r(k.prototype),"connectedCallback",this).call(this),this._attached=!0}},{kind:"method",key:"disconnectedCallback",value:function(){i(r(k.prototype),"disconnectedCallback",this).call(this),this._attached=!1}},{kind:"method",key:"render",value:function(){return this._attached&&this.hass&&this.stateObj?o`
      <ha-camera-stream
        .hass=${this.hass}
        .stateObj=${this.stateObj}
        allow-exoplayer
        controls
      ></ha-camera-stream>
      ${this._cameraPrefs?o`
            <ha-formfield label="Preload stream">
              <ha-checkbox
                .checked=${this._cameraPrefs.preload_stream}
                @change=${this._handleCheckboxChanged}
              >
              </ha-checkbox>
            </ha-formfield>
          `:void 0}
    `:o``}},{kind:"method",key:"updated",value:function(t){if(!t.has("stateObj"))return;const e=t.get("stateObj"),a=e?e.entity_id:void 0,s=this.stateObj?this.stateObj.entity_id:void 0;s!==a&&s&&d(this.hass,"stream")&&h(this.stateObj,n)&&this.stateObj.attributes.frontend_stream_type===l&&this._fetchCameraPrefs()}},{kind:"method",key:"_fetchCameraPrefs",value:async function(){this._cameraPrefs=await m(this.hass,this.stateObj.entity_id)}},{kind:"method",key:"_handleCheckboxChanged",value:async function(t){const e=t.currentTarget;try{this._cameraPrefs=await f(this.hass,this.stateObj.entity_id,{preload_stream:e.checked})}catch(t){alert(t.message),e.checked=!e.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      :host {
        display: block;
        position: relative;
      }
      ha-formfield {
        position: absolute;
        top: 0;
        right: 0;
        background-color: var(--secondary-background-color);
        padding-right: 16px;
        border-bottom-left-radius: 4px;
      }
    `}}]}}),e);customElements.define("more-info-camera",k);
