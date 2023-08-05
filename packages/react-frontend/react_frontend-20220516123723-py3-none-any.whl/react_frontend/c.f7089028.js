import{_ as t,s as i,e as s,$ as e,ar as o,n as a}from"./main-ac83c92b.js";import{a as r}from"./c.c7eb9fb9.js";import{f as n}from"./c.9f624ee3.js";import{m as l,n as c,o as h,F as d}from"./c.3e14cfd3.js";import"./c.5756eeee.js";import"./c.027db416.js";import"./c.8cbd7110.js";t([a("more-info-cover")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){if(!this.stateObj)return e``;const t=l(this.stateObj);return e`
      <div class=${this._computeClassNames(this.stateObj)}>
        <div class="current_position">
          <ha-labeled-slider
            .caption=${this.hass.localize("ui.card.cover.position")}
            pin=""
            .value=${this.stateObj.attributes.current_position}
            .disabled=${!c(this.stateObj)}
            @change=${this._coverPositionSliderChanged}
          ></ha-labeled-slider>
        </div>

        <div class="tilt">
          ${h(this.stateObj)?e` <ha-labeled-slider
                .caption=${this.hass.localize("ui.card.cover.tilt_position")}
                pin=""
                extra=""
                .value=${this.stateObj.attributes.current_tilt_position}
                @change=${this._coverTiltPositionSliderChanged}
              >
                ${t?e``:e`<ha-cover-tilt-controls
                      .hass=${this.hass}
                      slot="extra"
                      .stateObj=${this.stateObj}
                    ></ha-cover-tilt-controls> `}
              </ha-labeled-slider>`:t?e``:e`
                <div class="title">
                  ${this.hass.localize("ui.card.cover.tilt_position")}
                </div>
                <ha-cover-tilt-controls
                  .hass=${this.hass}
                  .stateObj=${this.stateObj}
                ></ha-cover-tilt-controls>
              `}
        </div>
      </div>
      <ha-attributes
        .hass=${this.hass}
        .stateObj=${this.stateObj}
        extra-filters="current_position,current_tilt_position"
      ></ha-attributes>
    `}},{kind:"method",key:"_computeClassNames",value:function(t){return[r(t,["current_position","current_tilt_position"]),n(t,d)].join(" ")}},{kind:"method",key:"_coverPositionSliderChanged",value:function(t){this.hass.callService("cover","set_cover_position",{entity_id:this.stateObj.entity_id,position:t.target.value})}},{kind:"method",key:"_coverTiltPositionSliderChanged",value:function(t){this.hass.callService("cover","set_cover_tilt_position",{entity_id:this.stateObj.entity_id,tilt_position:t.target.value})}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      .current_position,
      .tilt {
        max-height: 0px;
        overflow: hidden;
      }

      .has-set_position .current_position,
      .has-current_position .current_position,
      .has-open_tilt .tilt,
      .has-close_tilt .tilt,
      .has-stop_tilt .tilt,
      .has-set_tilt_position .tilt,
      .has-current_tilt_position .tilt {
        max-height: 208px;
      }

      /* from ha-labeled-slider for consistent look */
      .title {
        margin: 5px 0 8px;
        color: var(--primary-text-color);
      }
    `}}]}}),i);
