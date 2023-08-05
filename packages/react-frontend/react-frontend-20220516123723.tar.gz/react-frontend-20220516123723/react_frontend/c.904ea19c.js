import{_ as e,n as t,s as i,e as a,t as s,m as r,$ as n,aA as d,f as o,aq as c,ar as l}from"./main-ac83c92b.js";import{au as h,av as p,aw as u,ax as m,ay as y,az as v}from"./c.3e14cfd3.js";import{H as f}from"./c.213328e9.js";import{F as g}from"./c.f5888e17.js";import"./c.0660f3f3.js";import{U as k}from"./c.027db416.js";e([t("hui-card-element-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"getConfigElement",value:async function(){const e=await h(this.configElementType);if(e&&e.getConfigElement)return e.getConfigElement()}}]}}),f);const _=["zone","persistent_notification"],w=(e,t)=>{if("call-service"!==t.action||!t.service_data||!t.service_data.entity_id)return;let i=t.service_data.entity_id;Array.isArray(i)||(i=[i]);for(const t of i)e.add(t)},E=(e,t)=>{"string"!=typeof t?(t.entity&&e.add(t.entity),t.camera_image&&e.add(t.camera_image),t.tap_action&&w(e,t.tap_action),t.hold_action&&w(e,t.hold_action)):e.add(t)},b=(e,t)=>{t.entity&&E(e,t.entity),t.entities&&Array.isArray(t.entities)&&t.entities.forEach((t=>E(e,t))),t.card&&b(e,t.card),t.cards&&Array.isArray(t.cards)&&t.cards.forEach((t=>b(e,t))),t.elements&&Array.isArray(t.elements)&&t.elements.forEach((t=>b(e,t))),t.badges&&Array.isArray(t.badges)&&t.badges.forEach((t=>E(e,t)))},x=[{type:"alarm-panel",showElement:!0},{type:"button",showElement:!0},{type:"calendar",showElement:!0},{type:"entities",showElement:!0},{type:"entity",showElement:!0},{type:"gauge",showElement:!0},{type:"glance",showElement:!0},{type:"history-graph",showElement:!0},{type:"statistics-graph",showElement:!1},{type:"humidifier",showElement:!0},{type:"light",showElement:!0},{type:"map",showElement:!0},{type:"markdown",showElement:!0},{type:"media-control",showElement:!0},{type:"picture",showElement:!0},{type:"picture-elements",showElement:!0},{type:"picture-entity",showElement:!0},{type:"picture-glance",showElement:!0},{type:"plant-status",showElement:!0},{type:"sensor",showElement:!0},{type:"thermostat",showElement:!0},{type:"weather-forecast",showElement:!0},{type:"area",showElement:!0},{type:"conditional"},{type:"entity-filter"},{type:"grid"},{type:"horizontal-stack"},{type:"iframe"},{type:"logbook"},{type:"vertical-stack"},{type:"shopping-list"}];e([t("hui-card-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_cards",value:()=>[]},{kind:"field",key:"lovelace",value:void 0},{kind:"field",key:"cardPicked",value:void 0},{kind:"field",decorators:[s()],key:"_filter",value:()=>""},{kind:"field",decorators:[s()],key:"_width",value:void 0},{kind:"field",decorators:[s()],key:"_height",value:void 0},{kind:"field",key:"_unusedEntities",value:void 0},{kind:"field",key:"_usedEntities",value:void 0},{kind:"field",key:"_filterCards",value:()=>r(((e,t)=>{if(!t)return e;let i=e.map((e=>e.card));const a=new g(i,{keys:["type","name","description"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2});return i=a.search(t).map((e=>e.item)),e.filter((e=>i.includes(e.card)))}))},{kind:"method",key:"render",value:function(){return this.hass&&this.lovelace&&this._unusedEntities&&this._usedEntities?n`
      <search-input
        .hass=${this.hass}
        .filter=${this._filter}
        @value-changed=${this._handleSearchChange}
        .label=${this.hass.localize("ui.panel.lovelace.editor.edit_card.search_cards")}
      ></search-input>
      <div
        id="content"
        style=${d({width:this._width?`${this._width}px`:"auto",height:this._height?`${this._height}px`:"auto"})}
      >
        <div class="cards-container">
          ${this._filterCards(this._cards,this._filter).map((e=>e.element))}
        </div>
        <div class="cards-container">
          <div
            class="card manual"
            @click=${this._cardPicked}
            .config=${{type:""}}
          >
            <div class="card-header">
              ${this.hass.localize("ui.panel.lovelace.editor.card.generic.manual")}
            </div>
            <div class="preview description">
              ${this.hass.localize("ui.panel.lovelace.editor.card.generic.manual_description")}
            </div>
          </div>
        </div>
      </div>
    `:n``}},{kind:"method",key:"shouldUpdate",value:function(e){const t=e.get("hass");return!t||t.locale!==this.hass.locale}},{kind:"method",key:"firstUpdated",value:function(){if(!this.hass||!this.lovelace)return;const e=(e=>{const t=new Set;return e.views.forEach((e=>b(t,e))),t})(this.lovelace),t=((e,t)=>{const i=new Set;for(const a of Object.keys(e.states))t.has(a)||_.includes(a.split(".",1)[0])||i.add(a);return i})(this.hass,e);this._usedEntities=[...e].filter((e=>this.hass.states[e]&&!k.includes(this.hass.states[e].state))),this._unusedEntities=[...t].filter((e=>this.hass.states[e]&&!k.includes(this.hass.states[e].state))),this._loadCards()}},{kind:"method",key:"_loadCards",value:function(){let e=x.map((e=>({name:this.hass.localize(`ui.panel.lovelace.editor.card.${e.type}.name`),description:this.hass.localize(`ui.panel.lovelace.editor.card.${e.type}.description`),...e})));p.length>0&&(e=e.concat(p.map((e=>({type:e.type,name:e.name,description:e.description,showElement:e.preview,isCustom:!0}))))),this._cards=e.map((e=>({card:e,element:n`${u(this._renderCardElement(e),n`
          <div class="card spinner">
            <ha-circular-progress active alt="Loading"></ha-circular-progress>
          </div>
        `)}`})))}},{kind:"method",key:"_handleSearchChange",value:function(e){const t=e.detail.value;if(t){if(!this._width||!this._height){const e=this.shadowRoot.getElementById("content");if(e&&!this._width){const t=e.clientWidth;t&&(this._width=t)}if(e&&!this._height){const t=e.clientHeight;t&&(this._height=t)}}}else this._width=void 0,this._height=void 0;this._filter=t}},{kind:"method",key:"_cardPicked",value:function(e){const t=e.currentTarget.config;o(this,"config-changed",{config:t})}},{kind:"method",key:"_tryCreateCardElement",value:function(e){const t=m(e);return t.hass=this.hass,t.addEventListener("ll-rebuild",(i=>{i.stopPropagation(),this._rebuildCard(t,e)}),{once:!0}),t}},{kind:"method",key:"_rebuildCard",value:function(e,t){let i;try{i=this._tryCreateCardElement(t)}catch(e){return}e.parentElement&&e.parentElement.replaceChild(i,e)}},{kind:"method",key:"_renderCardElement",value:async function(e){let{type:t}=e;const{showElement:i,isCustom:a,name:s,description:r}=e,d=a?y(t):void 0;let o;a&&(t=`${v}${t}`);let l={type:t};if(this.hass&&this.lovelace&&(l=await(async(e,t,i,a)=>{let s={type:t};const r=await h(t);if(r&&r.getStubConfig){const t=await r.getStubConfig(e,i,a);s={...s,...t}}return s})(this.hass,t,this._unusedEntities,this._usedEntities),i))try{o=this._tryCreateCardElement(l)}catch(e){o=void 0}return n`
      <div class="card">
        <div
          class="overlay"
          @click=${this._cardPicked}
          .config=${l}
        ></div>
        <div class="card-header">
          ${d?`${this.hass.localize("ui.panel.lovelace.editor.cardpicker.custom_card")}: ${d.name||d.type}`:s}
        </div>
        <div
          class="preview ${c({description:!o||"HUI-ERROR-CARD"===o.tagName})}"
        >
          ${o&&"HUI-ERROR-CARD"!==o.tagName?o:d?d.description||this.hass.localize("ui.panel.lovelace.editor.cardpicker.no_description"):r}
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[l`
        search-input {
          display: block;
          --mdc-shape-small: var(--card-picker-search-shape);
          margin: var(--card-picker-search-margin);
        }

        .cards-container {
          display: grid;
          grid-gap: 8px 8px;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          margin-top: 20px;
        }

        .card {
          height: 100%;
          max-width: 500px;
          display: flex;
          flex-direction: column;
          border-radius: var(--ha-card-border-radius, 4px);
          background: var(--primary-background-color, #fafafa);
          cursor: pointer;
          position: relative;
        }

        .card-header {
          color: var(--ha-card-header-color, --primary-text-color);
          font-family: var(--ha-card-header-font-family, inherit);
          font-size: 16px;
          font-weight: bold;
          letter-spacing: -0.012em;
          line-height: 20px;
          padding: 12px 16px;
          display: block;
          text-align: center;
          background: var(
            --ha-card-background,
            var(--card-background-color, white)
          );
          border-bottom: 1px solid var(--divider-color);
        }

        .preview {
          pointer-events: none;
          margin: 20px;
          flex-grow: 1;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .preview > :first-child {
          zoom: 0.6;
          display: block;
          width: 100%;
        }

        .description {
          text-align: center;
        }

        .spinner {
          align-items: center;
          justify-content: center;
        }

        .overlay {
          position: absolute;
          width: 100%;
          height: 100%;
          z-index: 1;
          box-sizing: border-box;
          border: var(--ha-card-border-width, 1px) solid
            var(--ha-card-border-color, var(--divider-color));
          border-radius: var(--ha-card-border-radius, 4px);
        }

        .manual {
          max-width: none;
        }
      `]}}]}}),i);
