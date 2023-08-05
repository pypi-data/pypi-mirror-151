import{_ as t,s as e,e as s,t as a,$ as i,aq as r,g as o,i as n,ar as l,n as d}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";import"./c.a4895d0e.js";import{U as h,z as c,A as u,ai as b,aj as f,y as v,ak as m,al as p,am as k}from"./c.027db416.js";import"./c.c8193d47.js";import"./c.f731f3b4.js";import"./c.8cbd7110.js";import"./c.47fa9be3.js";import"./c.d2605417.js";t([d("ha-faded")],(function(t,e){class d extends e{constructor(...e){super(...e),t(this)}}return{F:d,d:[{kind:"field",decorators:[s({type:Number,attribute:"faded-height"})],key:"fadedHeight",value:()=>102},{kind:"field",decorators:[a()],key:"_contentShown",value:()=>!1},{kind:"method",key:"render",value:function(){return i`
      <div
        class="container ${r({faded:!this._contentShown})}"
        style=${this._contentShown?"":`max-height: ${this.fadedHeight}px`}
        @click=${this._showContent}
      >
        <slot
          @iron-resize=${this._setShowContent}
        ></slot>
      </div>
    `}},{kind:"get",key:"_slottedHeight",value:function(){var t;return(null===(t=this.shadowRoot.querySelector(".container"))||void 0===t?void 0:t.firstElementChild).assignedElements().reduce(((t,e)=>t+e.offsetHeight),0)||0}},{kind:"method",key:"_setShowContent",value:function(){const t=this._slottedHeight;this._contentShown=0!==t&&t<=this.fadedHeight+50}},{kind:"method",key:"firstUpdated",value:function(t){o(n(d.prototype),"firstUpdated",this).call(this,t),this._setShowContent()}},{kind:"method",key:"_showContent",value:function(){this._contentShown=!0}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      .container {
        display: block;
        height: auto;
        cursor: default;
      }
      .faded {
        cursor: pointer;
        -webkit-mask-image: linear-gradient(
          to bottom,
          black 25%,
          transparent 100%
        );
        mask-image: linear-gradient(to bottom, black 25%, transparent 100%);
        overflow-y: hidden;
      }
    `}}]}}),e),t([d("more-info-update")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[a()],key:"_releaseNotes",value:void 0},{kind:"field",decorators:[a()],key:"_error",value:void 0},{kind:"method",key:"render",value:function(){var t,e;if(!this.hass||!this.stateObj||h.includes(this.stateObj.state))return i``;const s=this.stateObj.attributes.latest_version&&this.stateObj.attributes.skipped_version===this.stateObj.attributes.latest_version;return i`
      ${this.stateObj.attributes.in_progress?c(this.stateObj,u)&&"number"==typeof this.stateObj.attributes.in_progress?i`<mwc-linear-progress
              .progress=${this.stateObj.attributes.in_progress/100}
              buffer=""
            ></mwc-linear-progress>`:i`<mwc-linear-progress indeterminate></mwc-linear-progress>`:""}
      ${this.stateObj.attributes.title?i`<h3>${this.stateObj.attributes.title}</h3>`:""}
      ${this._error?i`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}

      <div class="row">
        <div class="key">
          ${this.hass.localize("ui.dialogs.more_info_control.update.installed_version")}
        </div>
        <div class="value">
          ${null!==(t=this.stateObj.attributes.installed_version)&&void 0!==t?t:this.hass.localize("state.default.unavailable")}
        </div>
      </div>
      <div class="row">
        <div class="key">
          ${this.hass.localize("ui.dialogs.more_info_control.update.latest_version")}
        </div>
        <div class="value">
          ${null!==(e=this.stateObj.attributes.latest_version)&&void 0!==e?e:this.hass.localize("state.default.unavailable")}
        </div>
      </div>

      ${this.stateObj.attributes.release_url?i`<div class="row">
            <div class="key">
              <a
                href=${this.stateObj.attributes.release_url}
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.dialogs.more_info_control.update.release_announcement")}
              </a>
            </div>
          </div>`:""}
      ${c(this.stateObj,b)&&!this._error?void 0===this._releaseNotes?i`<ha-circular-progress active></ha-circular-progress>`:i`<hr />
              <ha-faded>
                <ha-markdown .content=${this._releaseNotes}></ha-markdown>
              </ha-faded> `:this.stateObj.attributes.release_summary?i`<hr />
            <ha-markdown
              .content=${this.stateObj.attributes.release_summary}
            ></ha-markdown>`:""}
      ${c(this.stateObj,f)?i`<hr />
            <ha-formfield
              .label=${this.hass.localize("ui.dialogs.more_info_control.update.create_backup")}
            >
              <ha-checkbox
                checked
                .disabled=${v(this.stateObj)}
              ></ha-checkbox>
            </ha-formfield> `:""}
      <hr />
      <div class="actions">
        ${this.stateObj.attributes.auto_update?"":i`
              <mwc-button
                @click=${this._handleSkip}
                .disabled=${s||"off"===this.stateObj.state||v(this.stateObj)}
              >
                ${this.hass.localize("ui.dialogs.more_info_control.update.skip")}
              </mwc-button>
            `}
        ${c(this.stateObj,m)?i`
              <mwc-button
                @click=${this._handleInstall}
                .disabled=${"off"===this.stateObj.state&&!s||v(this.stateObj)}
              >
                ${this.hass.localize("ui.dialogs.more_info_control.update.install")}
              </mwc-button>
            `:""}
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(){c(this.stateObj,b)&&p(this.hass,this.stateObj.entity_id).then((t=>{this._releaseNotes=t})).catch((t=>{this._error=t.message}))}},{kind:"get",key:"_shouldCreateBackup",value:function(){var t;if(!c(this.stateObj,f))return null;const e=null===(t=this.shadowRoot)||void 0===t?void 0:t.querySelector("ha-checkbox");return!e||e.checked}},{kind:"method",key:"_handleInstall",value:function(){const t={entity_id:this.stateObj.entity_id};this._shouldCreateBackup&&(t.backup=!0),c(this.stateObj,k)&&this.stateObj.attributes.latest_version&&(t.version=this.stateObj.attributes.latest_version),this.hass.callService("update","install",t)}},{kind:"method",key:"_handleSkip",value:function(){this.hass.callService("update","skip",{entity_id:this.stateObj.entity_id})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      hr {
        border-color: var(--divider-color);
        border-bottom: none;
        margin: 16px 0;
      }
      ha-expansion-panel {
        margin: 16px 0;
      }
      .row {
        margin: 0;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }
      .actions {
        margin: 8px 0 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
      }

      .actions mwc-button {
        margin: 0 4px 4px;
      }
      a {
        color: var(--primary-color);
      }
      ha-circular-progress {
        width: 100%;
        justify-content: center;
      }
      mwc-linear-progress {
        margin-bottom: -10px;
        margin-top: -10px;
      }
    `}}]}}),e);
