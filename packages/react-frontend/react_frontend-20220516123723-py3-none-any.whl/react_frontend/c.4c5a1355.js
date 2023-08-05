import{f as e,_ as t,s as i,e as n,$ as o,ed as a,cD as s,dD as l,ar as c,n as d,t as r,g as h,i as u,el as f,ap as g,em as m}from"./main-ac83c92b.js";import{ai as p,_ as v,aj as _,ak as y,Y as k,a3 as b,Z as $,a1 as E,a7 as C,$ as w,a6 as x,a2 as j,a5 as z,a4 as M,al as S,X as V,a0 as I}from"./c.3e14cfd3.js";import{a as A}from"./c.2541228c.js";import{e as T}from"./c.027db416.js";import"./c.86ce6bc8.js";import{T as F,e as B}from"./c.60f8b094.js";import{h as D}from"./c.1bf1ded5.js";import{i as P}from"./c.6e13c00f.js";import"./c.53212acc.js";import{s as R,p as G}from"./c.cb759a4c.js";import{H as U}from"./c.213328e9.js";import{a as q}from"./c.1430be7b.js";import{b as H}from"./c.461e571b.js";import{c as O}from"./c.ad12eed4.js";import"./c.8cbd7110.js";import"./c.cfa85e17.js";import"./c.0e001851.js";import"./c.d6711a1d.js";import"./c.c018532e.js";import"./c.622dfac1.js";import"./c.1fca9ca6.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";const W=e=>e.startsWith("custom:"),X=()=>import("./c.0ac4b8ff.js");let Y;t([d("hui-header-footer-editor")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",key:"lovelaceConfig",value:void 0},{kind:"field",decorators:[n({attribute:!1})],key:"config",value:void 0},{kind:"field",decorators:[n()],key:"configValue",value:void 0},{kind:"method",key:"render",value:function(){var e,t,i;return o`
      <div>
        <span>
          ${this.hass.localize(`ui.panel.lovelace.editor.header-footer.${this.configValue}`)}:
          ${null!==(e=this.config)&&void 0!==e&&e.type?this.hass.localize(`ui.panel.lovelace.editor.header-footer.types.${null===(t=this.config)||void 0===t?void 0:t.type}.name`):this.hass.localize("ui.panel.lovelace.editor.common.none")}
        </span>
      </div>
      <div>
        ${null!==(i=this.config)&&void 0!==i&&i.type?o`
              <ha-icon-button
                .label=${this.hass.localize("ui.panel.lovelace.editor.common.clear")}
                .path=${s}
                class="remove-icon"
                @click=${this._delete}
              ></ha-icon-button>
              <ha-icon-button
                .label=${this.hass.localize("ui.panel.lovelace.editor.common.edit")}
                .path=${l}
                class="edit-icon"
                @click=${this._edit}
              ></ha-icon-button>
            `:o`
              <ha-icon-button
                .label=${this.hass.localize("ui.panel.lovelace.editor.common.add")}
                .path=${a}
                class="add-icon"
                @click=${this._add}
              ></ha-icon-button>
            `}
      </div>
    `}},{kind:"method",key:"_edit",value:function(){e(this,"edit-detail-element",{subElementConfig:{elementConfig:this.config,type:this.configValue}})}},{kind:"method",key:"_add",value:function(){var t,i;t=this,i={pickHeaderFooter:e=>this._elementPicked(e),type:this.configValue},e(t,"show-dialog",{dialogTag:"hui-dialog-create-headerfooter",dialogImport:X,dialogParams:i})}},{kind:"method",key:"_elementPicked",value:function(t){e(this,"value-changed",{value:t}),e(this,"edit-detail-element",{subElementConfig:{elementConfig:t,type:this.configValue}})}},{kind:"method",key:"_delete",value:function(){e(this,"value-changed",{value:""})}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      :host {
        font-size: 16px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
      }

      :host > div {
        display: flex;
        align-items: center;
      }

      ha-icon-button,
      .header-footer-icon {
        --mdc-icon-button-size: 36px;
        color: var(--secondary-text-color);
      }

      .header-footer-icon {
        padding-right: 8px;
      }
    `}}]}}),i),t([d("hui-entities-card-row-editor")],(function(t,i){class a extends i{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",decorators:[n({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[n({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[n()],key:"label",value:void 0},{kind:"field",decorators:[r()],key:"_attached",value:()=>!1},{kind:"field",decorators:[r()],key:"_renderEmptySortable",value:()=>!1},{kind:"field",key:"_sortable",value:void 0},{kind:"method",key:"connectedCallback",value:function(){h(u(a.prototype),"connectedCallback",this).call(this),this._attached=!0}},{kind:"method",key:"disconnectedCallback",value:function(){h(u(a.prototype),"disconnectedCallback",this).call(this),this._attached=!1}},{kind:"method",key:"render",value:function(){return this.entities&&this.hass?o`
      <h3>
        ${this.label||`${this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})`}
      </h3>
      <div class="entities">
        ${P([this.entities,this._renderEmptySortable],(()=>this._renderEmptySortable?"":this.entities.map(((e,t)=>o`
                  <div class="entity">
                    <ha-svg-icon class="handle" .path=${f}></ha-svg-icon>
                    ${e.type?o`
                          <div class="special-row">
                            <div>
                              <span>
                                ${this.hass.localize(`ui.panel.lovelace.editor.card.entities.entity_row.${e.type}`)}
                              </span>
                              <span class="secondary"
                                >${this.hass.localize("ui.panel.lovelace.editor.card.entities.edit_special_row")}</span
                              >
                            </div>
                          </div>
                        `:o`
                          <ha-entity-picker
                            allow-custom-entity
                            hideClearIcon
                            .hass=${this.hass}
                            .value=${e.entity}
                            .index=${t}
                            @value-changed=${this._valueChanged}
                          ></ha-entity-picker>
                        `}
                    <ha-icon-button
                      .label=${this.hass.localize("ui.components.entity.entity-picker.clear")}
                      .path=${s}
                      class="remove-icon"
                      .index=${t}
                      @click=${this._removeRow}
                    ></ha-icon-button>
                    <ha-icon-button
                      .label=${this.hass.localize("ui.components.entity.entity-picker.edit")}
                      .path=${l}
                      class="edit-icon"
                      .index=${t}
                      @click=${this._editRow}
                    ></ha-icon-button>
                  </div>
                `))))}
      </div>
      <ha-entity-picker
        class="add-entity"
        .hass=${this.hass}
        @value-changed=${this._addEntity}
      ></ha-entity-picker>
    `:o``}},{kind:"method",key:"updated",value:function(e){h(u(a.prototype),"updated",this).call(this,e);const t=e.has("_attached"),i=e.has("entities");if(i||t){var n;if(t&&!this._attached)return null===(n=this._sortable)||void 0===n||n.destroy(),void(this._sortable=void 0);this._sortable||!this.entities?i&&this._handleEntitiesChanged():this._createSortable()}}},{kind:"method",key:"_handleEntitiesChanged",value:async function(){this._renderEmptySortable=!0,await this.updateComplete;const e=this.shadowRoot.querySelector(".entities");for(;e.lastElementChild;)e.removeChild(e.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_createSortable",value:async function(){if(!Y){const e=await import("./c.b354e590.js");Y=e.Sortable,Y.mount(e.OnSpill),Y.mount(e.AutoScroll())}this._sortable=new Y(this.shadowRoot.querySelector(".entities"),{animation:150,fallbackClass:"sortable-fallback",handle:".handle",onEnd:async e=>this._rowMoved(e)})}},{kind:"method",key:"_addEntity",value:async function(t){const i=t.detail.value;if(""===i)return;const n=this.entities.concat({entity:i});t.target.value="",e(this,"entities-changed",{entities:n})}},{kind:"method",key:"_rowMoved",value:function(t){if(t.oldIndex===t.newIndex)return;const i=this.entities.concat();i.splice(t.newIndex,0,i.splice(t.oldIndex,1)[0]),e(this,"entities-changed",{entities:i})}},{kind:"method",key:"_removeRow",value:function(t){const i=t.currentTarget.index,n=this.entities.concat();n.splice(i,1),e(this,"entities-changed",{entities:n})}},{kind:"method",key:"_valueChanged",value:function(t){const i=t.detail.value,n=t.target.index,o=this.entities.concat();""===i||void 0===i?o.splice(n,1):o[n]={...o[n],entity:i},e(this,"entities-changed",{entities:o})}},{kind:"method",key:"_editRow",value:function(t){const i=t.currentTarget.index;e(this,"edit-detail-element",{subElementConfig:{index:i,type:"row",elementConfig:this.entities[i]}})}},{kind:"get",static:!0,key:"styles",value:function(){return[R,c`
        ha-entity-picker {
          margin-top: 8px;
        }
        .add-entity {
          display: block;
          margin-left: 31px;
          margin-right: 71px;
        }
        .entity {
          display: flex;
          align-items: center;
        }

        .entity .handle {
          padding-right: 8px;
          cursor: move;
        }

        .entity ha-entity-picker {
          flex-grow: 1;
        }

        .special-row {
          height: 60px;
          font-size: 16px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          flex-grow: 1;
        }

        .special-row div {
          display: flex;
          flex-direction: column;
        }

        .remove-icon,
        .edit-icon {
          --mdc-icon-button-size: 36px;
          color: var(--secondary-text-color);
        }

        .secondary {
          font-size: 12px;
          color: var(--secondary-text-color);
        }
      `]}}]}}),i);t([d("hui-row-element-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"get",key:"configElementType",value:function(){var e,t;return null!==(e=this.value)&&void 0!==e&&e.type||!("entity"in this.value)?null===(t=this.value)||void 0===t?void 0:t.type:"generic-row"}},{kind:"method",key:"getConfigElement",value:async function(){if("generic-row"===this.configElementType)return document.createElement("hui-generic-entity-row-editor");const e=await _(this.configElementType);return e&&e.getConfigElement?e.getConfigElement():void 0}}]}}),U),t([d("hui-headerfooter-element-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"getConfigElement",value:async function(){const e=await y(this.configElementType);if(e&&e.getConfigElement)return e.getConfigElement()}}]}}),U),t([d("hui-sub-element-editor")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[n({attribute:!1})],key:"config",value:void 0},{kind:"field",decorators:[r()],key:"_guiModeAvailable",value:()=>!0},{kind:"field",decorators:[r()],key:"_guiMode",value:()=>!0},{kind:"field",decorators:[g(".editor")],key:"_editorElement",value:void 0},{kind:"method",key:"render",value:function(){var e;return o`
      <div class="header">
        <div class="back-title">
          <ha-icon-button
            .label=${this.hass.localize("ui.common.back")}
            .path=${m}
            @click=${this._goBack}
          ></ha-icon-button>
          <span slot="title"
            >${this.hass.localize(`ui.panel.lovelace.editor.sub-element-editor.types.${null===(e=this.config)||void 0===e?void 0:e.type}`)}</span
          >
        </div>
        <mwc-button
          slot="secondaryAction"
          .disabled=${!this._guiModeAvailable}
          @click=${this._toggleMode}
        >
          ${this.hass.localize(this._guiMode?"ui.panel.lovelace.editor.edit_card.show_code_editor":"ui.panel.lovelace.editor.edit_card.show_visual_editor")}
        </mwc-button>
      </div>
      ${"row"===this.config.type?o`
            <hui-row-element-editor
              class="editor"
              .hass=${this.hass}
              .value=${this.config.elementConfig}
              @config-changed=${this._handleConfigChanged}
              @GUImode-changed=${this._handleGUIModeChanged}
            ></hui-row-element-editor>
          `:"header"===this.config.type||"footer"===this.config.type?o`
            <hui-headerfooter-element-editor
              class="editor"
              .hass=${this.hass}
              .value=${this.config.elementConfig}
              @config-changed=${this._handleConfigChanged}
              @GUImode-changed=${this._handleGUIModeChanged}
            ></hui-headerfooter-element-editor>
          `:""}
    `}},{kind:"method",key:"_goBack",value:function(){e(this,"go-back")}},{kind:"method",key:"_toggleMode",value:function(){var e;null===(e=this._editorElement)||void 0===e||e.toggleMode()}},{kind:"method",key:"_handleGUIModeChanged",value:function(e){e.stopPropagation(),this._guiMode=e.detail.guiMode,this._guiModeAvailable=e.detail.guiModeAvailable}},{kind:"method",key:"_handleConfigChanged",value:function(e){this._guiModeAvailable=e.detail.guiModeAvailable}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .back-title {
        display: flex;
        align-items: center;
        font-size: 18px;
      }
    `}}]}}),i);const Z=k({type:b("button"),entity:$(v()),name:$(v()),icon:$(v()),action_name:$(v()),tap_action:q,hold_action:$(q),double_tap_action:$(q)}),J=k({type:b("cast"),view:E([v(),C()]),dashboard:$(v()),name:$(v()),icon:$(v()),hide_if_unavailable:$(w())}),K=k({type:b("call-service"),name:v(),service:v(),icon:$(v()),action_name:$(v()),service_data:$(x())}),L=k({type:b("conditional"),row:x(),conditions:j(k({entity:v(),state:$(v()),state_not:$(v())}))}),N=k({type:b("divider"),style:$(x())}),Q=k({type:b("section"),label:$(v())}),ee=k({type:b("weblink"),url:v(),name:$(v()),icon:$(v())}),te=k({type:b("buttons"),entities:j(E([k({entity:v(),name:$(v()),icon:$(v()),image:$(v()),show_name:$(w()),show_icon:$(w()),tap_action:$(q),hold_action:$(q),double_tap_action:$(q)}),v()]))}),ie=k({type:b("attribute"),entity:v(),attribute:v(),prefix:$(v()),suffix:$(v()),name:$(v()),icon:$(v()),format:$(z(F))}),ne=k({type:b("text"),name:v(),text:v(),icon:$(v())}),oe=M({type:p(v(),"custom element type",W)}),ae=S((e=>{if(e&&"object"==typeof e&&"type"in e){if(W(e.type))return oe;switch(e.type){case"attribute":return ie;case"button":return Z;case"buttons":return te;case"call-service":return K;case"cast":return J;case"conditional":return L;case"divider":return N;case"section":return Q;case"text":return ne;case"weblink":return ee}}return B})),se=V(H,k({title:$(E([v(),w()])),entity:$(A()),theme:$(v()),icon:$(v()),show_header_toggle:$(w()),state_color:$(w()),entities:j(ae),header:$(D),footer:$(D)}));let le=t([d("hui-entities-card-editor")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[n({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[r()],key:"_config",value:void 0},{kind:"field",decorators:[r()],key:"_configEntities",value:void 0},{kind:"field",decorators:[r()],key:"_subElementEditorConfig",value:void 0},{kind:"method",key:"setConfig",value:function(e){I(e,se),this._config=e,this._configEntities=G(e.entities)}},{kind:"get",key:"_title",value:function(){return this._config.title||""}},{kind:"get",key:"_theme",value:function(){return this._config.theme||""}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?this._subElementEditorConfig?o`
        <hui-sub-element-editor
          .hass=${this.hass}
          .config=${this._subElementEditorConfig}
          @go-back=${this._goBack}
          @config-changed=${this._handleSubElementChanged}
        >
        </hui-sub-element-editor>
      `:o`
      <div class="card-config">
        <ha-textfield
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.title")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value=${this._title}
          .configValue=${"title"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-theme-picker
          .hass=${this.hass}
          .value=${this._theme}
          .label=${`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`}
          .configValue=${"theme"}
          @value-changed=${this._valueChanged}
        ></ha-theme-picker>
        <div class="side-by-side">
          <ha-formfield
            .label=${this.hass.localize("ui.panel.lovelace.editor.card.entities.show_header_toggle")}
            .dir=${T(this.hass)}
          >
            <ha-switch
              .checked=${!1!==this._config.show_header_toggle}
              .configValue=${"show_header_toggle"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
          <ha-formfield
            .label=${this.hass.localize("ui.panel.lovelace.editor.card.generic.state_color")}
            .dir=${T(this.hass)}
          >
            <ha-switch
              .checked=${this._config.state_color}
              .configValue=${"state_color"}
              @change=${this._valueChanged}
            ></ha-switch>
          </ha-formfield>
        </div>
        <hui-header-footer-editor
          .hass=${this.hass}
          .configValue=${"header"}
          .config=${this._config.header}
          @value-changed=${this._valueChanged}
          @edit-detail-element=${this._editDetailElement}
        ></hui-header-footer-editor>
        <hui-header-footer-editor
          .hass=${this.hass}
          .configValue=${"footer"}
          .config=${this._config.footer}
          @value-changed=${this._valueChanged}
          @edit-detail-element=${this._editDetailElement}
        ></hui-header-footer-editor>
      </div>
      <hui-entities-card-row-editor
        .hass=${this.hass}
        .entities=${this._configEntities}
        @entities-changed=${this._valueChanged}
        @edit-detail-element=${this._editDetailElement}
      ></hui-entities-card-row-editor>
    `:o``}},{kind:"method",key:"_valueChanged",value:function(t){var i;if(t.stopPropagation(),!this._config||!this.hass)return;const n=t.target,o=n.configValue||(null===(i=this._subElementEditorConfig)||void 0===i?void 0:i.type),a=void 0!==n.checked?n.checked:n.value||t.detail.config||t.detail.value;if(!("title"===o&&n.value===this._title||"theme"===o&&n.value===this._theme)){if("row"===o||t.detail&&t.detail.entities){const e=t.detail.entities||this._configEntities.concat();"row"===o&&(a?e[this._subElementEditorConfig.index]=a:(e.splice(this._subElementEditorConfig.index,1),this._goBack()),this._subElementEditorConfig.elementConfig=a),this._config={...this._config,entities:e},this._configEntities=G(this._config.entities)}else o&&(""===a?(this._config={...this._config},delete this._config[o]):this._config={...this._config,[o]:a});e(this,"config-changed",{config:this._config})}}},{kind:"method",key:"_handleSubElementChanged",value:function(t){var i;if(t.stopPropagation(),!this._config||!this.hass)return;const n=null===(i=this._subElementEditorConfig)||void 0===i?void 0:i.type,o=t.detail.config;if("row"===n){const e=this._configEntities.concat();o?e[this._subElementEditorConfig.index]=o:(e.splice(this._subElementEditorConfig.index,1),this._goBack()),this._config={...this._config,entities:e},this._configEntities=G(this._config.entities)}else n&&(""===o?(this._config={...this._config},delete this._config[n]):this._config={...this._config,[n]:o});this._subElementEditorConfig={...this._subElementEditorConfig,elementConfig:o},e(this,"config-changed",{config:this._config})}},{kind:"method",key:"_editDetailElement",value:function(e){this._subElementEditorConfig=e.detail.subElementConfig}},{kind:"method",key:"_goBack",value:function(){this._subElementEditorConfig=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[O,c`
        .edit-entity-row-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 18px;
        }

        hui-header-footer-editor {
          padding-top: 4px;
        }

        ha-textfield {
          display: block;
          margin-bottom: 16px;
        }
      `]}}]}}),i);export{le as HuiEntitiesCardEditor};
