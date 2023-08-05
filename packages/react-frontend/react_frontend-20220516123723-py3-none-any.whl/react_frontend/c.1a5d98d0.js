import{_ as e,s as t,e as i,t as s,ap as a,g as n,i as r,f as o,$ as c,eP as d,ar as l,n as h,eQ as u,bh as _,bj as v,dF as p,h as y}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";import{c as g}from"./c.8cbd7110.js";import{s as m}from"./c.027db416.js";import"./c.e9aa747b.js";import"./c.8eddd911.js";let f,k,b,S;var w,$;e([h("ha-qr-scanner")],(function(e,t){class h extends t{constructor(...t){super(...t),e(this)}}return{F:h,d:[{kind:"field",decorators:[i()],key:"localize",value:void 0},{kind:"field",decorators:[s()],key:"_cameras",value:void 0},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",key:"_qrScanner",value:void 0},{kind:"field",key:"_qrNotFoundCount",value:()=>0},{kind:"field",decorators:[a("video",!0)],key:"_video",value:void 0},{kind:"field",decorators:[a("#canvas-container",!0)],key:"_canvasContainer",value:void 0},{kind:"field",decorators:[a("ha-textfield")],key:"_manualInput",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){for(n(r(h.prototype),"disconnectedCallback",this).call(this),this._qrNotFoundCount=0,this._qrScanner&&(this._qrScanner.stop(),this._qrScanner.destroy(),this._qrScanner=void 0);this._canvasContainer.lastChild;)this._canvasContainer.removeChild(this._canvasContainer.lastChild)}},{kind:"method",key:"connectedCallback",value:function(){n(r(h.prototype),"connectedCallback",this).call(this),this.hasUpdated&&navigator.mediaDevices&&this._loadQrScanner()}},{kind:"method",key:"firstUpdated",value:function(){navigator.mediaDevices&&this._loadQrScanner()}},{kind:"method",key:"updated",value:function(e){e.has("_error")&&this._error&&o(this,"qr-code-error",{message:this._error})}},{kind:"method",key:"render",value:function(){return c`${this._error?c`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
    ${navigator.mediaDevices?c`<video></video>
          <div id="canvas-container">
            ${this._cameras&&this._cameras.length>1?c`<ha-button-menu
                  corner="BOTTOM_START"
                  fixed
                  @closed=${m}
                >
                  <ha-icon-button
                    slot="trigger"
                    .label=${this.localize("ui.components.qr-scanner.select_camera")}
                    .path=${d}
                  ></ha-icon-button>
                  ${this._cameras.map((e=>c`
                      <mwc-list-item
                        .value=${e.id}
                        @click=${this._cameraChanged}
                        >${e.label}</mwc-list-item
                      >
                    `))}
                </ha-button-menu>`:""}
          </div>`:c`<ha-alert alert-type="warning">
            ${window.isSecureContext?this.localize("ui.components.qr-scanner.not_supported"):this.localize("ui.components.qr-scanner.only_https_supported")}
          </ha-alert>
          <p>${this.localize("ui.components.qr-scanner.manual_input")}</p>
          <div class="row">
            <ha-textfield
              .label=${this.localize("ui.components.qr-scanner.enter_qr_code")}
              @keyup=${this._manualKeyup}
              @paste=${this._manualPaste}
            ></ha-textfield>
            <mwc-button @click=${this._manualSubmit}
              >${this.localize("ui.common.submit")}</mwc-button
            >
          </div>`}`}},{kind:"method",key:"_loadQrScanner",value:async function(){const e=(await import("./c.091e3af5.js")).default;if(!await e.hasCamera())return void(this._error="No camera found");e.WORKER_PATH="/static/js/qr-scanner-worker.min.js",this._listCameras(e),this._qrScanner=new e(this._video,this._qrCodeScanned,this._qrCodeError);const t=this._qrScanner.$canvas;this._canvasContainer.appendChild(t),t.style.display="block";try{await this._qrScanner.start()}catch(e){this._error=e}}},{kind:"method",key:"_listCameras",value:async function(e){this._cameras=await e.listCameras(!0)}},{kind:"field",key:"_qrCodeError",value(){return e=>{if("No QR code found"===e)return this._qrNotFoundCount++,void(250===this._qrNotFoundCount&&(this._error=e));this._error=e.message||e,console.log(e)}}},{kind:"field",key:"_qrCodeScanned",value(){return async e=>{this._qrNotFoundCount=0,o(this,"qr-code-scanned",{value:e})}}},{kind:"method",key:"_manualKeyup",value:function(e){"Enter"===e.key&&this._qrCodeScanned(e.target.value)}},{kind:"method",key:"_manualPaste",value:function(e){this._qrCodeScanned((e.clipboardData||window.clipboardData).getData("text"))}},{kind:"method",key:"_manualSubmit",value:function(){this._qrCodeScanned(this._manualInput.value)}},{kind:"method",key:"_cameraChanged",value:function(e){var t;null===(t=this._qrScanner)||void 0===t||t.setCamera(e.target.value)}},{kind:"field",static:!0,key:"styles",value:()=>l`
    canvas {
      width: 100%;
    }
    #canvas-container {
      position: relative;
    }
    ha-button-menu {
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: #727272b2;
      color: white;
      border-radius: 50%;
    }
    .row {
      display: flex;
      align-items: center;
    }
    ha-textfield {
      flex: 1;
      margin-right: 8px;
    }
  `}]}}),t),function(e){e[e.Idle=0]="Idle",e[e.Including=1]="Including",e[e.Excluding=2]="Excluding",e[e.Busy=3]="Busy",e[e.SmartStart=4]="SmartStart"}(f||(f={})),function(e){e[e.Default=0]="Default",e[e.SmartStart=1]="SmartStart",e[e.Insecure=2]="Insecure",e[e.Security_S0=3]="Security_S0",e[e.Security_S2=4]="Security_S2"}(k||(k={})),function(e){e[e.Temporary=-2]="Temporary",e[e.None=-1]="None",e[e.S2_Unauthenticated=0]="S2_Unauthenticated",e[e.S2_Authenticated=1]="S2_Authenticated",e[e.S2_AccessControl=2]="S2_AccessControl",e[e.S0_Legacy=7]="S0_Legacy"}(b||(b={})),function(e){e[e.SmartStart=0]="SmartStart"}(S||(S={})),function(e){e[e.S2=0]="S2",e[e.SmartStart=1]="SmartStart"}(w||(w={})),function(e){e[e.ZWave=0]="ZWave",e[e.ZWaveLongRange=1]="ZWaveLongRange"}($||($={}));let C;!function(e){e[e.Unknown=0]="Unknown",e[e.Asleep=1]="Asleep",e[e.Awake=2]="Awake",e[e.Dead=3]="Dead",e[e.Alive=4]="Alive"}(C||(C={}));const q=(e,t,i,s)=>e.callWS({type:"zwave_js/grant_security_classes",entry_id:t,security_classes:i,client_side_auth:s});e([h("dialog-zwave_js-add-node")],(function(e,t){class d extends t{constructor(...t){super(...t),e(this)}}return{F:d,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_params",value:void 0},{kind:"field",decorators:[s()],key:"_entryId",value:void 0},{kind:"field",decorators:[s()],key:"_status",value:void 0},{kind:"field",decorators:[s()],key:"_device",value:void 0},{kind:"field",decorators:[s()],key:"_stages",value:void 0},{kind:"field",decorators:[s()],key:"_inclusionStrategy",value:void 0},{kind:"field",decorators:[s()],key:"_dsk",value:void 0},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",decorators:[s()],key:"_requestedGrant",value:void 0},{kind:"field",decorators:[s()],key:"_securityClasses",value:()=>[]},{kind:"field",decorators:[s()],key:"_lowSecurity",value:()=>!1},{kind:"field",decorators:[s()],key:"_supportsSmartStart",value:void 0},{kind:"field",key:"_addNodeTimeoutHandle",value:void 0},{kind:"field",key:"_subscribed",value:void 0},{kind:"field",key:"_qrProcessing",value:()=>!1},{kind:"method",key:"disconnectedCallback",value:function(){n(r(d.prototype),"disconnectedCallback",this).call(this),this._unsubscribe()}},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._entryId=e.entry_id,this._status="loading",this._checkSmartStartSupport(),this._startInclusion()}},{kind:"field",decorators:[a("#pin-input")],key:"_pinInput",value:void 0},{kind:"method",key:"render",value:function(){var e;return this._entryId?c`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${g(this.hass,this.hass.localize("ui.panel.config.zwave_js.add_node.title"))}
      >
        ${"loading"===this._status?c`<div style="display: flex; justify-content: center;">
              <ha-circular-progress size="large" active></ha-circular-progress>
            </div>`:"choose_strategy"===this._status?c`<h3>Choose strategy</h3>
              <div class="flex-column">
                <ha-formfield
                  .label=${c`<b>Secure if possible</b>
                    <div class="secondary">
                      Requires user interaction during inclusion. Fast and
                      secure with S2 when supported. Fallback to legacy S0 or no
                      encryption when necessary.
                    </div>`}
                >
                  <ha-radio
                    name="strategy"
                    @change=${this._handleStrategyChange}
                    .value=${k.Default}
                    .checked=${this._inclusionStrategy===k.Default||void 0===this._inclusionStrategy}
                  >
                  </ha-radio>
                </ha-formfield>
                <ha-formfield
                  .label=${c`<b>Legacy Secure</b>
                    <div class="secondary">
                      Uses the older S0 security that is secure, but slow due to
                      a lot of overhead. Allows securely including S2 capable
                      devices which fail to be included with S2.
                    </div>`}
                >
                  <ha-radio
                    name="strategy"
                    @change=${this._handleStrategyChange}
                    .value=${k.Security_S0}
                    .checked=${this._inclusionStrategy===k.Security_S0}
                  >
                  </ha-radio>
                </ha-formfield>
                <ha-formfield
                  .label=${c`<b>Insecure</b>
                    <div class="secondary">Do not use encryption.</div>`}
                >
                  <ha-radio
                    name="strategy"
                    @change=${this._handleStrategyChange}
                    .value=${k.Insecure}
                    .checked=${this._inclusionStrategy===k.Insecure}
                  >
                  </ha-radio>
                </ha-formfield>
              </div>
              <mwc-button
                slot="primaryAction"
                @click=${this._startManualInclusion}
              >
                Search device
              </mwc-button>`:"qr_scan"===this._status?c`${this._error?c`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
              <ha-qr-scanner
                .localize=${this.hass.localize}
                @qr-code-scanned=${this._qrCodeScanned}
              ></ha-qr-scanner>
              <mwc-button slot="secondaryAction" @click=${this._startOver}>
                ${this.hass.localize("ui.panel.config.zwave_js.common.back")}
              </mwc-button>`:"validate_dsk_enter_pin"===this._status?c`
                <p>
                  Please enter the 5-digit PIN for your device and verify that
                  the rest of the device-specific key matches the one that can
                  be found on your device or the manual.
                </p>
                ${this._error?c`<ha-alert alert-type="error">
                        ${this._error}
                      </ha-alert>`:""}
                <div class="flex-container">
                <ha-textfield
                  label="PIN"
                  id="pin-input"
                  @keyup=${this._handlePinKeyUp}
                ></ha-textfield>
                ${this._dsk}
                </div>
                <mwc-button
                  slot="primaryAction"
                  @click=${this._validateDskAndEnterPin}
                >
                  Submit
                </mwc-button>
              </div>
            `:"grant_security_classes"===this._status?c`
              <h3>The device has requested the following security classes:</h3>
              ${this._error?c`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
              <div class="flex-column">
                ${null===(e=this._requestedGrant)||void 0===e?void 0:e.securityClasses.sort().reverse().map((e=>c`<ha-formfield
                      .label=${c`<b
                          >${this.hass.localize(`ui.panel.config.zwave_js.security_classes.${b[e]}.title`)}</b
                        >
                        <div class="secondary">
                          ${this.hass.localize(`ui.panel.config.zwave_js.security_classes.${b[e]}.description`)}
                        </div>`}
                    >
                      <ha-checkbox
                        @change=${this._handleSecurityClassChange}
                        .value=${e}
                        .checked=${this._securityClasses.includes(e)}
                      >
                      </ha-checkbox>
                    </ha-formfield>`))}
              </div>
              <mwc-button
                slot="primaryAction"
                .disabled=${!this._securityClasses.length}
                @click=${this._grantSecurityClasses}
              >
                Submit
              </mwc-button>
            `:"timed_out"===this._status?c`
              <h3>Timed out!</h3>
              <p>
                We have not found any device in inclusion mode. Make sure the
                device is active and in inclusion mode.
              </p>
              <mwc-button slot="primaryAction" @click=${this._startOver}>
                Retry
              </mwc-button>
            `:"started_specific"===this._status?c`<h3>
                ${this.hass.localize("ui.panel.config.zwave_js.add_node.searching_device")}
              </h3>
              <ha-circular-progress active></ha-circular-progress>
              <p>
                ${this.hass.localize("ui.panel.config.zwave_js.add_node.follow_device_instructions")}
              </p>`:"started"===this._status?c`
              <div class="select-inclusion">
                <div class="outline">
                  <h2>
                    ${this.hass.localize("ui.panel.config.zwave_js.add_node.searching_device")}
                  </h2>
                  <ha-circular-progress active></ha-circular-progress>
                  <p>
                    ${this.hass.localize("ui.panel.config.zwave_js.add_node.follow_device_instructions")}
                  </p>
                  <p>
                    <button
                      class="link"
                      @click=${this._chooseInclusionStrategy}
                    >
                      ${this.hass.localize("ui.panel.config.zwave_js.add_node.choose_inclusion_strategy")}
                    </button>
                  </p>
                </div>
                ${this._supportsSmartStart?c` <div class="outline">
                      <h2>
                        ${this.hass.localize("ui.panel.config.zwave_js.add_node.qr_code")}
                      </h2>
                      <ha-svg-icon .path=${u}></ha-svg-icon>
                      <p>
                        ${this.hass.localize("ui.panel.config.zwave_js.add_node.qr_code_paragraph")}
                      </p>
                      <p>
                        <mwc-button @click=${this._scanQRCode}>
                          ${this.hass.localize("ui.panel.config.zwave_js.add_node.scan_qr_code")}
                        </mwc-button>
                      </p>
                    </div>`:""}
              </div>
              <mwc-button slot="primaryAction" @click=${this.closeDialog}>
                ${this.hass.localize("ui.common.cancel")}
              </mwc-button>
            `:"interviewing"===this._status?c`
              <div class="flex-container">
                <ha-circular-progress active></ha-circular-progress>
                <div class="status">
                  <p>
                    <b
                      >${this.hass.localize("ui.panel.config.zwave_js.add_node.interview_started")}</b
                    >
                  </p>
                  ${this._stages?c` <div class="stages">
                        ${this._stages.map((e=>c`
                            <span class="stage">
                              <ha-svg-icon
                                .path=${_}
                                class="success"
                              ></ha-svg-icon>
                              ${e}
                            </span>
                          `))}
                      </div>`:""}
                </div>
              </div>
              <mwc-button slot="primaryAction" @click=${this.closeDialog}>
                ${this.hass.localize("ui.common.close")}
              </mwc-button>
            `:"failed"===this._status?c`
              <div class="flex-container">
                <div class="status">
                  <ha-alert
                    alert-type="error"
                    .title=${this.hass.localize("ui.panel.config.zwave_js.add_node.inclusion_failed")}
                  >
                    ${this._error||this.hass.localize("ui.panel.config.zwave_js.add_node.check_logs")}
                  </ha-alert>
                  ${this._stages?c` <div class="stages">
                        ${this._stages.map((e=>c`
                            <span class="stage">
                              <ha-svg-icon
                                .path=${_}
                                class="success"
                              ></ha-svg-icon>
                              ${e}
                            </span>
                          `))}
                      </div>`:""}
                </div>
              </div>
              <mwc-button slot="primaryAction" @click=${this.closeDialog}>
                ${this.hass.localize("ui.panel.config.zwave_js.common.close")}
              </mwc-button>
            `:"finished"===this._status?c`
              <div class="flex-container">
                <ha-svg-icon
                  .path=${this._lowSecurity?v:_}
                  class=${this._lowSecurity?"warning":"success"}
                ></ha-svg-icon>
                <div class="status">
                  <p>
                    ${this.hass.localize("ui.panel.config.zwave_js.add_node.inclusion_finished")}
                  </p>
                  ${this._lowSecurity?c`<ha-alert
                        alert-type="warning"
                        title="The device was added insecurely"
                      >
                        There was an error during secure inclusion. You can try
                        again by excluding the device and adding it again.
                      </ha-alert>`:""}
                  <a href=${`/config/devices/device/${this._device.id}`}>
                    <mwc-button>
                      ${this.hass.localize("ui.panel.config.zwave_js.add_node.view_device")}
                    </mwc-button>
                  </a>
                  ${this._stages?c` <div class="stages">
                        ${this._stages.map((e=>c`
                            <span class="stage">
                              <ha-svg-icon
                                .path=${_}
                                class="success"
                              ></ha-svg-icon>
                              ${e}
                            </span>
                          `))}
                      </div>`:""}
                </div>
              </div>
              <mwc-button slot="primaryAction" @click=${this.closeDialog}>
                ${this.hass.localize("ui.panel.config.zwave_js.common.close")}
              </mwc-button>
            `:"provisioned"===this._status?c` <div class="flex-container">
                <ha-svg-icon
                  .path=${_}
                  class="success"
                ></ha-svg-icon>
                <div class="status">
                  <p>
                    ${this.hass.localize("ui.panel.config.zwave_js.add_node.provisioning_finished")}
                  </p>
                </div>
              </div>
              <mwc-button slot="primaryAction" @click=${this.closeDialog}>
                ${this.hass.localize("ui.panel.config.zwave_js.common.close")}
              </mwc-button>`:""}
      </ha-dialog>
    `:c``}},{kind:"method",key:"_chooseInclusionStrategy",value:function(){this._unsubscribe(),this._status="choose_strategy"}},{kind:"method",key:"_handleStrategyChange",value:function(e){this._inclusionStrategy=e.target.value}},{kind:"method",key:"_handleSecurityClassChange",value:function(e){const t=e.currentTarget,i=Number(t.value);t.checked&&!this._securityClasses.includes(i)?this._securityClasses=[...this._securityClasses,i]:t.checked||(this._securityClasses=this._securityClasses.filter((e=>e!==i)))}},{kind:"method",key:"_scanQRCode",value:async function(){this._unsubscribe(),this._status="qr_scan"}},{kind:"method",key:"_qrCodeScanned",value:function(e){this._qrProcessing||this._handleQrCodeScanned(e.detail.value)}},{kind:"method",key:"_handleQrCodeScanned",value:async function(e){if(this._error=void 0,"qr_scan"!==this._status||this._qrProcessing)return;if(this._qrProcessing=!0,e.length<52||!e.startsWith("90"))return this._qrProcessing=!1,void(this._error=`Invalid QR code (${e})`);let t;try{t=await(i=this.hass,s=this._entryId,a=e,i.callWS({type:"zwave_js/parse_qr_code_string",entry_id:s,qr_code_string:a}))}catch(e){return this._qrProcessing=!1,void(this._error=e.message)}var i,s,a;if(this._status="loading",this.updateComplete.then((()=>{this._qrProcessing=!1})),1===t.version)try{var n;await((e,t,i,s,a)=>e.callWS({type:"zwave_js/provision_smart_start_node",entry_id:t,qr_code_string:s,qr_provisioning_information:i,planned_provisioning_entry:a}))(this.hass,this._entryId,t),this._status="provisioned",null!==(n=this._params)&&void 0!==n&&n.addedCallback&&this._params.addedCallback()}catch(e){this._error=e.message,this._status="failed"}else 0===t.version?(this._inclusionStrategy=k.Security_S2,this._startInclusion(t)):(this._error="This QR code is not supported",this._status="failed")}},{kind:"method",key:"_handlePinKeyUp",value:function(e){"Enter"===e.key&&this._validateDskAndEnterPin()}},{kind:"method",key:"_validateDskAndEnterPin",value:async function(){this._status="loading",this._error=void 0;try{await(e=this.hass,t=this._entryId,i=this._pinInput.value,e.callWS({type:"zwave_js/validate_dsk_and_enter_pin",entry_id:t,pin:i}))}catch(e){this._error=e.message,this._status="validate_dsk_enter_pin"}var e,t,i}},{kind:"method",key:"_grantSecurityClasses",value:async function(){this._status="loading",this._error=void 0;try{await q(this.hass,this._entryId,this._securityClasses)}catch(e){this._error=e.message,this._status="grant_security_classes"}}},{kind:"method",key:"_startManualInclusion",value:function(){this._inclusionStrategy||(this._inclusionStrategy=k.Default),this._startInclusion()}},{kind:"method",key:"_checkSmartStartSupport",value:async function(){var e,t,i;this._supportsSmartStart=(await(e=this.hass,t=this._entryId,i=S.SmartStart,e.callWS({type:"zwave_js/supports_feature",entry_id:t,feature:i}))).supported}},{kind:"method",key:"_startOver",value:function(e){this._startInclusion()}},{kind:"method",key:"_startInclusion",value:function(e,t,i){if(!this.hass)return;this._lowSecurity=!1;const s=e||t||i;this._subscribed=((e,t,i,s=k.Default,a,n,r)=>e.connection.subscribeMessage((e=>i(e)),{type:"zwave_js/add_node",entry_id:t,inclusion_strategy:s,qr_code_string:n,qr_provisioning_information:a,planned_provisioning_entry:r}))(this.hass,this._entryId,(e=>{if("inclusion started"===e.event&&(this._status=s?"started_specific":"started"),"inclusion failed"===e.event&&(this._unsubscribe(),this._status="failed"),"inclusion stopped"===e.event&&(this._addNodeTimeoutHandle&&clearTimeout(this._addNodeTimeoutHandle),this._addNodeTimeoutHandle=void 0),"validate dsk and enter pin"===e.event&&(this._status="validate_dsk_enter_pin",this._dsk=e.dsk),"grant security classes"===e.event){if(void 0===this._inclusionStrategy)return void q(this.hass,this._entryId,e.requested_grant.securityClasses,e.requested_grant.clientSideAuth);this._requestedGrant=e.requested_grant,this._securityClasses=e.requested_grant.securityClasses,this._status="grant_security_classes"}var t;("device registered"===e.event&&(this._device=e.device),"node added"===e.event&&(this._status="interviewing",this._lowSecurity=e.node.low_security),"interview completed"===e.event)&&(this._unsubscribe(),this._status="finished",null!==(t=this._params)&&void 0!==t&&t.addedCallback&&this._params.addedCallback());"interview stage completed"===e.event&&(void 0===this._stages?this._stages=[e.stage]:this._stages=[...this._stages,e.stage])}),this._inclusionStrategy,e,t,i),this._addNodeTimeoutHandle=window.setTimeout((()=>{this._unsubscribe(),this._status="timed_out"}),9e4)}},{kind:"method",key:"_unsubscribe",value:function(){var e,t;this._subscribed&&(this._subscribed.then((e=>e())),this._subscribed=void 0),this._entryId&&(e=this.hass,t=this._entryId,e.callWS({type:"zwave_js/stop_inclusion",entry_id:t})),this._requestedGrant=void 0,this._dsk=void 0,this._securityClasses=[],this._status=void 0,this._addNodeTimeoutHandle&&clearTimeout(this._addNodeTimeoutHandle),this._addNodeTimeoutHandle=void 0}},{kind:"method",key:"closeDialog",value:function(){this._unsubscribe(),this._inclusionStrategy=void 0,this._entryId=void 0,this._status=void 0,this._device=void 0,this._stages=void 0,this._error=void 0,o(this,"dialog-closed",{dialog:this.localName})}},{kind:"get",static:!0,key:"styles",value:function(){return[p,y,l`
        h3 {
          margin-top: 0;
        }

        .success {
          color: var(--success-color);
        }

        .warning {
          color: var(--warning-color);
        }

        .stages {
          margin-top: 16px;
          display: grid;
        }

        .flex-container .stage ha-svg-icon {
          width: 16px;
          height: 16px;
          margin-right: 0px;
        }
        .stage {
          padding: 8px;
        }

        .flex-container {
          display: flex;
          align-items: center;
        }

        .flex-column {
          display: flex;
          flex-direction: column;
        }

        .flex-column ha-formfield {
          padding: 8px 0;
        }

        .select-inclusion {
          display: flex;
          align-items: center;
        }

        .select-inclusion .outline:nth-child(2) {
          margin-left: 16px;
        }

        .select-inclusion .outline {
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          padding: 16px;
          min-height: 250px;
          text-align: center;
          flex: 1;
        }

        @media all and (max-width: 500px) {
          .select-inclusion {
            flex-direction: column;
          }

          .select-inclusion .outline:nth-child(2) {
            margin-left: 0;
            margin-top: 16px;
          }
        }

        ha-svg-icon {
          width: 68px;
          height: 48px;
        }
        ha-textfield {
          display: block;
        }
        .secondary {
          color: var(--secondary-text-color);
        }

        .flex-container ha-circular-progress,
        .flex-container ha-svg-icon {
          margin-right: 20px;
        }
      `]}}]}}),t);
