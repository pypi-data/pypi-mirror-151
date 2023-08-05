import{_ as e,s as i,e as t,$ as n,f as s,ar as a,n as d}from"./main-ac83c92b.js";import{ag as l}from"./c.3e14cfd3.js";import"./c.53212acc.js";e([d("ha-entities-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"required",value:void 0},{kind:"field",decorators:[t()],key:"helper",value:void 0},{kind:"field",decorators:[t({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[t({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[t({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[t({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[t({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[t({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[t({attribute:"picked-entity-label"})],key:"pickedEntityLabel",value:void 0},{kind:"field",decorators:[t({attribute:"pick-entity-label"})],key:"pickEntityLabel",value:void 0},{kind:"field",decorators:[t()],key:"entityFilter",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return n``;const e=this._currentEntities;return n`
      ${e.map((e=>n`
          <div>
            <ha-entity-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeEntities=${this.includeEntities}
              .excludeEntities=${this.excludeEntities}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
              .entityFilter=${this._entityFilter}
              .value=${e}
              .label=${this.pickedEntityLabel}
              @value-changed=${this._entityChanged}
            ></ha-entity-picker>
          </div>
        `))}
      <div>
        <ha-entity-picker
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeEntities=${this.includeEntities}
          .excludeEntities=${this.excludeEntities}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
          .entityFilter=${this._entityFilter}
          .label=${this.pickEntityLabel}
          .helper=${this.helper}
          .required=${this.required&&!e.length}
          @value-changed=${this._addEntity}
        ></ha-entity-picker>
      </div>
    `}},{kind:"field",key:"_entityFilter",value(){return e=>(!this.value||!this.value.includes(e.entity_id))&&(!this.entityFilter||this.entityFilter(e))}},{kind:"get",key:"_currentEntities",value:function(){return this.value||[]}},{kind:"method",key:"_updateEntities",value:async function(e){this.value=e,s(this,"value-changed",{value:e})}},{kind:"method",key:"_entityChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;if(t===i||void 0!==t&&!l(t))return;const n=this._currentEntities;t&&!n.includes(t)?this._updateEntities(n.map((e=>e===i?t:e))):this._updateEntities(n.filter((e=>e!==i)))}},{kind:"method",key:"_addEntity",value:async function(e){e.stopPropagation();const i=e.detail.value;if(!i)return;if(e.currentTarget.value="",!i)return;const t=this._currentEntities;t.includes(i)||this._updateEntities([...t,i])}},{kind:"field",static:!0,key:"styles",value:()=>a`
    div {
      margin-top: 8px;
    }
  `}]}}),i);
