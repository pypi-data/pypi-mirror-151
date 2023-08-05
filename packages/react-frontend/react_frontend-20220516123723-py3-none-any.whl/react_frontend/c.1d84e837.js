import{_ as e,s as t,e as i,$ as a,dW as s,dr as o,ds as l,dt as n,du as d,dX as c,b0 as u,ar as r,n as h}from"./main-ac83c92b.js";import{z as m,x as _,w as v,e as b,s as p,i as y}from"./c.027db416.js";import{B as $,D as f,G as g,H as k,I as w,J as j,K as x,M,N as O}from"./c.3e14cfd3.js";import{s as C}from"./c.6999bfff.js";import"./c.8cbd7110.js";e([h("more-info-media_player")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){var e,t;if(!this.stateObj)return a``;const i=this.stateObj,r=$(i,!0);return a`
      <div class="controls">
        <div class="basic-controls">
          ${r?r.map((e=>a`
                  <ha-icon-button
                    action=${e.action}
                    @click=${this._handleClick}
                    .path=${e.icon}
                    .label=${this.hass.localize(`ui.card.media_player.${e.action}`)}
                  >
                  </ha-icon-button>
                `)):""}
        </div>
        ${m(i,f)?a`
              <mwc-button
                .label=${this.hass.localize("ui.card.media_player.browse_media")}
                @click=${this._showBrowseMedia}
              >
                <ha-svg-icon
                  .path=${s}
                  slot="icon"
                ></ha-svg-icon>
              </mwc-button>
            `:""}
      </div>
      ${!m(i,g)&&!m(i,k)||[_,v,"off"].includes(i.state)?"":a`
            <div class="volume">
              ${m(i,w)?a`
                    <ha-icon-button
                      .path=${i.attributes.is_volume_muted?o:l}
                      .label=${this.hass.localize("ui.card.media_player."+(i.attributes.is_volume_muted?"media_volume_unmute":"media_volume_mute"))}
                      @click=${this._toggleMute}
                    ></ha-icon-button>
                  `:""}
              ${m(i,k)?a`
                    <ha-icon-button
                      action="volume_down"
                      .path=${n}
                      .label=${this.hass.localize("ui.card.media_player.media_volume_down")}
                      @click=${this._handleClick}
                    ></ha-icon-button>
                    <ha-icon-button
                      action="volume_up"
                      .path=${d}
                      .label=${this.hass.localize("ui.card.media_player.media_volume_up")}
                      @click=${this._handleClick}
                    ></ha-icon-button>
                  `:""}
              ${m(i,g)?a`
                    <ha-slider
                      id="input"
                      pin
                      ignore-bar-touch
                      .dir=${b(this.hass)}
                      .value=${100*Number(i.attributes.volume_level)}
                      @change=${this._selectedValueChanged}
                    ></ha-slider>
                  `:""}
            </div>
          `}
      ${![_,v,"off"].includes(i.state)&&m(i,j)&&null!==(e=i.attributes.source_list)&&void 0!==e&&e.length?a`
            <div class="source-input">
              <ha-select
                .label=${this.hass.localize("ui.card.media_player.source")}
                icon
                .value=${i.attributes.source}
                @selected=${this._handleSourceChanged}
                fixedMenuPosition
                naturalMenuWidth
                @closed=${p}
              >
                ${i.attributes.source_list.map((e=>a`
                      <mwc-list-item .value=${e}>${e}</mwc-list-item>
                    `))}
                <ha-svg-icon .path=${c} slot="icon"></ha-svg-icon>
              </ha-select>
            </div>
          `:""}
      ${m(i,x)&&null!==(t=i.attributes.sound_mode_list)&&void 0!==t&&t.length?a`
            <div class="sound-input">
              <ha-select
                .label=${this.hass.localize("ui.card.media_player.sound_mode")}
                .value=${i.attributes.sound_mode}
                icon
                fixedMenuPosition
                naturalMenuWidth
                @selected=${this._handleSoundModeChanged}
                @closed=${p}
              >
                ${i.attributes.sound_mode_list.map((e=>a`
                    <mwc-list-item .value=${e}>${e}</mwc-list-item>
                  `))}
                <ha-svg-icon .path=${u} slot="icon"></ha-svg-icon>
              </ha-select>
            </div>
          `:""}
      ${y(this.hass,"tts")&&m(i,M)?a`
            <div class="tts">
              Text to speech has moved to the media browser.
            </div>
          `:""}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      ha-icon-button[action="turn_off"],
      ha-icon-button[action="turn_on"],
      ha-slider {
        flex-grow: 1;
      }

      .controls {
        display: flex;
        align-items: center;
        --mdc-theme-primary: currentColor;
      }

      .basic-controls {
        display: inline-flex;
        flex-grow: 1;
      }

      .volume,
      .source-input,
      .sound-input {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .source-input ha-select,
      .sound-input ha-select {
        margin-left: 10px;
        flex-grow: 1;
      }

      .tts {
        margin-top: 16px;
        font-style: italic;
      }

      mwc-button > ha-svg-icon {
        vertical-align: text-bottom;
      }
    `}},{kind:"method",key:"_handleClick",value:function(e){O(this.hass,this.stateObj,e.currentTarget.getAttribute("action"))}},{kind:"method",key:"_toggleMute",value:function(){this.hass.callService("media_player","volume_mute",{entity_id:this.stateObj.entity_id,is_volume_muted:!this.stateObj.attributes.is_volume_muted})}},{kind:"method",key:"_selectedValueChanged",value:function(e){this.hass.callService("media_player","volume_set",{entity_id:this.stateObj.entity_id,volume_level:Number(e.currentTarget.getAttribute("value"))/100})}},{kind:"method",key:"_handleSourceChanged",value:function(e){const t=e.target.value;t&&this.stateObj.attributes.source!==t&&this.hass.callService("media_player","select_source",{entity_id:this.stateObj.entity_id,source:t})}},{kind:"method",key:"_handleSoundModeChanged",value:function(e){var t;const i=e.target.value;i&&(null===(t=this.stateObj)||void 0===t?void 0:t.attributes.sound_mode)!==i&&this.hass.callService("media_player","select_sound_mode",{entity_id:this.stateObj.entity_id,sound_mode:i})}},{kind:"method",key:"_showBrowseMedia",value:function(){C(this,{action:"play",entityId:this.stateObj.entity_id,mediaPickedCallback:e=>this._playMedia(e.item.media_content_id,e.item.media_content_type)})}},{kind:"method",key:"_playMedia",value:function(e,t){this.hass.callService("media_player","play_media",{entity_id:this.stateObj.entity_id,media_content_id:e,media_content_type:t})}}]}}),t);
