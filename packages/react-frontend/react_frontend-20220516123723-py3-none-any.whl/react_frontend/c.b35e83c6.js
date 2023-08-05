import{_ as e,s as t,e as i,t as s,ap as a,g as d,i as c,di as o,$ as h,aq as n,ed as l,eG as r,eH as m,el as u,ar as p,n as _}from"./main-ac83c92b.js";import{i as k}from"./c.6e13c00f.js";import{a8 as g}from"./c.027db416.js";import"./c.3e14cfd3.js";import"./c.c8193d47.js";import{S as v}from"./c.02ed471c.js";import"./c.8cbd7110.js";import"./c.47fa9be3.js";const f=(e,t,i)=>e.callWS({type:"shopping_list/items/update",item_id:t,...i});let y;e([_("hui-shopping-list-card")],(function(e,t){class _ extends t{constructor(...t){super(...t),e(this)}}return{F:_,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.cbb8d52b.js"),document.createElement("hui-shopping-list-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"shopping-list"}}},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",decorators:[s()],key:"_uncheckedItems",value:void 0},{kind:"field",decorators:[s()],key:"_checkedItems",value:void 0},{kind:"field",decorators:[s()],key:"_reordering",value:()=>!1},{kind:"field",decorators:[s()],key:"_renderEmptySortable",value:()=>!1},{kind:"field",key:"_sortable",value:void 0},{kind:"field",decorators:[a("#sortable")],key:"_sortableEl",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3+(this._config&&this._config.title?2:0)}},{kind:"method",key:"setConfig",value:function(e){this._config=e,this._uncheckedItems=[],this._checkedItems=[]}},{kind:"method",key:"hassSubscribe",value:function(){return this._fetchData(),[this.hass.connection.subscribeEvents((()=>this._fetchData()),"shopping_list_updated")]}},{kind:"method",key:"updated",value:function(e){if(d(c(_.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),i=e.get("_config");(e.has("hass")&&(null==t?void 0:t.themes)!==this.hass.themes||e.has("_config")&&(null==i?void 0:i.theme)!==this._config.theme)&&o(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?h`
      <ha-card
        .header=${this._config.title}
        class=${n({"has-header":"title"in this._config})}
      >
        <div class="addRow">
          <ha-svg-icon
            class="addButton"
            .path=${l}
            .title=${this.hass.localize("ui.panel.lovelace.cards.shopping-list.add_item")}
            @click=${this._addItem}
          >
          </ha-svg-icon>
          <ha-textfield
            class="addBox"
            .placeholder=${this.hass.localize("ui.panel.lovelace.cards.shopping-list.add_item")}
            @keydown=${this._addKeyPress}
          ></ha-textfield>
          <ha-svg-icon
            class="reorderButton"
            .path=${r}
            .title=${this.hass.localize("ui.panel.lovelace.cards.shopping-list.reorder_items")}
            @click=${this._toggleReorder}
          >
          </ha-svg-icon>
        </div>
        ${this._reordering?h`
              <div id="sortable">
                ${k([this._uncheckedItems,this._renderEmptySortable],(()=>this._renderEmptySortable?"":this._renderItems(this._uncheckedItems)))}
              </div>
            `:this._renderItems(this._uncheckedItems)}
        ${this._checkedItems.length>0?h`
              <div class="divider"></div>
              <div class="checked">
                <span>
                  ${this.hass.localize("ui.panel.lovelace.cards.shopping-list.checked_items")}
                </span>
                <ha-svg-icon
                  class="clearall"
                  tabindex="0"
                  .path=${m}
                  .title=${this.hass.localize("ui.panel.lovelace.cards.shopping-list.clear_items")}
                  @click=${this._clearItems}
                >
                </ha-svg-icon>
              </div>
              ${g(this._checkedItems,(e=>e.id),(e=>h`
                    <div class="editRow">
                      <ha-checkbox
                        tabindex="0"
                        .checked=${e.complete}
                        .itemId=${e.id}
                        @change=${this._completeItem}
                      ></ha-checkbox>
                      <ha-textfield
                        class="item"
                        .value=${e.name}
                        .itemId=${e.id}
                        @change=${this._saveEdit}
                      ></ha-textfield>
                    </div>
                  `))}
            `:""}
      </ha-card>
    `:h``}},{kind:"method",key:"_renderItems",value:function(e){return h`
      ${g(e,(e=>e.id),(e=>h`
            <div class="editRow" item-id=${e.id}>
              <ha-checkbox
                tabindex="0"
                .checked=${e.complete}
                .itemId=${e.id}
                @change=${this._completeItem}
              ></ha-checkbox>
              <ha-textfield
                class="item"
                .value=${e.name}
                .itemId=${e.id}
                @change=${this._saveEdit}
              ></ha-textfield>
              ${this._reordering?h`
                    <ha-svg-icon
                      .title=${this.hass.localize("ui.panel.lovelace.cards.shopping-list.drag_and_drop")}
                      class="reorderButton"
                      .path=${u}
                    >
                    </ha-svg-icon>
                  `:""}
            </div>
          `))}
    `}},{kind:"method",key:"_fetchData",value:async function(){if(!this.hass)return;const e=[],t=[],i=await(s=this.hass,s.callWS({type:"shopping_list/items"}));var s;for(const s in i)i[s].complete?e.push(i[s]):t.push(i[s]);this._checkedItems=e,this._uncheckedItems=t}},{kind:"method",key:"_completeItem",value:function(e){f(this.hass,e.target.itemId,{complete:e.target.checked}).catch((()=>this._fetchData()))}},{kind:"method",key:"_saveEdit",value:function(e){f(this.hass,e.target.itemId,{name:e.target.value}).catch((()=>this._fetchData())),e.target.blur()}},{kind:"method",key:"_clearItems",value:function(){var e;this.hass&&(e=this.hass,e.callWS({type:"shopping_list/items/clear"})).catch((()=>this._fetchData()))}},{kind:"get",key:"_newItem",value:function(){return this.shadowRoot.querySelector(".addBox")}},{kind:"method",key:"_addItem",value:function(e){const t=this._newItem;var i,s;t.value.length>0&&(i=this.hass,s=t.value,i.callWS({type:"shopping_list/items/add",name:s})).catch((()=>this._fetchData())),t.value="",e&&t.focus()}},{kind:"method",key:"_addKeyPress",value:function(e){13===e.keyCode&&this._addItem(null)}},{kind:"method",key:"_toggleReorder",value:async function(){if(!y){const e=await import("./c.b354e590.js");y=e.Sortable}var e;(this._reordering=!this._reordering,await this.updateComplete,this._reordering)?this._createSortable():(null===(e=this._sortable)||void 0===e||e.destroy(),this._sortable=void 0)}},{kind:"method",key:"_createSortable",value:function(){const e=this._sortableEl;this._sortable=new y(e,{animation:150,fallbackClass:"sortable-fallback",dataIdAttr:"item-id",handle:"ha-svg-icon",onEnd:async t=>{var i,s;for(t.oldIndex!==t.newIndex&&((i=this.hass,s=this._sortable.toArray(),i.callWS({type:"shopping_list/items/reorder",item_ids:s})).catch((()=>this._fetchData())),this._uncheckedItems.splice(t.newIndex,0,this._uncheckedItems.splice(t.oldIndex,1)[0])),this._renderEmptySortable=!0,await this.updateComplete;null!=e&&e.lastElementChild;)e.removeChild(e.lastElementChild);this._renderEmptySortable=!1}})}},{kind:"get",static:!0,key:"styles",value:function(){return p`
      ha-card {
        padding: 16px;
        height: 100%;
        box-sizing: border-box;
      }

      .has-header {
        padding-top: 0;
      }

      .editRow,
      .addRow,
      .checked {
        display: flex;
        flex-direction: row;
        align-items: center;
      }

      .item {
        margin-top: 8px;
      }

      .addButton {
        padding-right: 16px;
        cursor: pointer;
      }

      .reorderButton {
        padding-left: 16px;
        cursor: pointer;
      }

      ha-checkbox {
        margin-left: -12px;
      }

      ha-textfield {
        flex-grow: 1;
      }

      .checked {
        margin: 12px 0;
        justify-content: space-between;
      }

      .checked span {
        color: var(--primary-text-color);
        font-weight: 500;
      }

      .divider {
        height: 1px;
        background-color: var(--divider-color);
        margin: 10px 0;
      }

      .clearall {
        cursor: pointer;
      }
    `}}]}}),v(t));
