import{_ as t,s as e,e as i,t as a,g as n,i as s,$ as d,el as o,f as l,ar as c,n as r}from"./main-ac83c92b.js";import{i as h}from"./c.6e13c00f.js";import"./c.53212acc.js";import{s as u}from"./c.cb759a4c.js";let y;t([r("hui-entity-editor")],(function(t,e){class r extends e{constructor(...e){super(...e),t(this)}}return{F:r,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[a()],key:"_attached",value:()=>!1},{kind:"field",decorators:[a()],key:"_renderEmptySortable",value:()=>!1},{kind:"field",key:"_sortable",value:void 0},{kind:"method",key:"connectedCallback",value:function(){n(s(r.prototype),"connectedCallback",this).call(this),this._attached=!0}},{kind:"method",key:"disconnectedCallback",value:function(){n(s(r.prototype),"disconnectedCallback",this).call(this),this._attached=!1}},{kind:"method",key:"render",value:function(){return this.entities?d`
      <h3>
        ${this.label||this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")+" ("+this.hass.localize("ui.panel.lovelace.editor.card.config.required")+")"}
      </h3>
      <div class="entities">
        ${h([this.entities,this._renderEmptySortable],(()=>this._renderEmptySortable?"":this.entities.map(((t,e)=>d`
                  <div class="entity" data-entity-id=${t.entity}>
                    <ha-svg-icon .path=${o}></ha-svg-icon>
                    <ha-entity-picker
                      .hass=${this.hass}
                      .value=${t.entity}
                      .index=${e}
                      @value-changed=${this._valueChanged}
                      allow-custom-entity
                    ></ha-entity-picker>
                  </div>
                `))))}
      </div>
      <ha-entity-picker
        class="add-entity"
        .hass=${this.hass}
        @value-changed=${this._addEntity}
      ></ha-entity-picker>
    `:d``}},{kind:"method",key:"updated",value:function(t){n(s(r.prototype),"updated",this).call(this,t);const e=t.has("_attached"),i=t.has("entities");if(i||e){var a;if(e&&!this._attached)return null===(a=this._sortable)||void 0===a||a.destroy(),void(this._sortable=void 0);this._sortable||!this.entities?i&&this._handleEntitiesChanged():this._createSortable()}}},{kind:"method",key:"_handleEntitiesChanged",value:async function(){this._renderEmptySortable=!0,await this.updateComplete;const t=this.shadowRoot.querySelector(".entities");for(;t.lastElementChild;)t.removeChild(t.lastElementChild);this._renderEmptySortable=!1}},{kind:"method",key:"_createSortable",value:async function(){if(!y){const t=await import("./c.b354e590.js");y=t.Sortable,y.mount(t.OnSpill),y.mount(t.AutoScroll())}this._sortable=new y(this.shadowRoot.querySelector(".entities"),{animation:150,fallbackClass:"sortable-fallback",handle:"ha-svg-icon",dataIdAttr:"data-entity-id",onEnd:async t=>this._entityMoved(t)})}},{kind:"method",key:"_addEntity",value:async function(t){const e=t.detail.value;if(""===e)return;const i=this.entities.concat({entity:e});t.target.value="",l(this,"entities-changed",{entities:i})}},{kind:"method",key:"_entityMoved",value:function(t){if(t.oldIndex===t.newIndex)return;const e=this.entities.concat();e.splice(t.newIndex,0,e.splice(t.oldIndex,1)[0]),l(this,"entities-changed",{entities:e})}},{kind:"method",key:"_valueChanged",value:function(t){const e=t.detail.value,i=t.target.index,a=this.entities.concat();""===e||void 0===e?a.splice(i,1):a[i]={...a[i],entity:e},l(this,"entities-changed",{entities:a})}},{kind:"get",static:!0,key:"styles",value:function(){return[u,c`
        ha-entity-picker {
          margin-top: 8px;
        }
        .add-entity {
          display: block;
          margin-left: 31px;
        }
        .entity {
          display: flex;
          align-items: center;
        }
        .entity ha-svg-icon {
          padding-right: 8px;
          cursor: move;
        }
        .entity ha-entity-picker {
          flex-grow: 1;
        }
      `]}}]}}),e);
