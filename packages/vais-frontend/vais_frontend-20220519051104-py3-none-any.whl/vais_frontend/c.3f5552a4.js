import{a as e,f as i,e as a,t,i as s,$ as o,av as n,o as r,j as l,r as d,n as c,V as h,m as p,O as m,P as v,aw as u,X as g,Y as y,ax as f,al as x,am as _,ag as k,s as b,d as $}from"./main-e088bb19.js";import{a as w}from"./c.166c4b5c.js";import"./c.e9faf9fb.js";import{n as z}from"./c.2b12d4b5.js";import{s as j}from"./c.d8002660.js";import{m as R}from"./c.73230ac7.js";import{u as C}from"./c.e60bf0f8.js";import"./c.3c6412dd.js";import"./c.14628ea3.js";import"./c.743a15a1.js";import"./c.7943fa91.js";import"./c.8e28b461.js";e([c("ha-expansion-panel")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[a({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[a()],key:"header",value:void 0},{kind:"field",decorators:[a()],key:"secondary",value:void 0},{kind:"field",decorators:[t()],key:"_showContent",value(){return this.expanded}},{kind:"field",decorators:[s(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return o`
      <div
        id="summary"
        @click=${this._toggleContainer}
        @keydown=${this._toggleContainer}
        role="button"
        tabindex="0"
        aria-expanded=${this.expanded}
        aria-controls="sect1"
      >
        <slot class="header" name="header">
          ${this.header}
          <slot class="secondary" name="secondary">${this.secondary}</slot>
        </slot>
        <ha-svg-icon
          .path=${n}
          class="summary-icon ${r({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${r({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?o`<slot></slot>`:""}
      </div>
    `}},{kind:"method",key:"willUpdate",value:function(e){e.has("expanded")&&this.expanded&&(this._showContent=this.expanded)}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height"),this._showContent=this.expanded}},{kind:"method",key:"_toggleContainer",value:async function(e){if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;e.preventDefault();const i=!this.expanded;l(this,"expanded-will-change",{expanded:i}),i&&(this._showContent=!0,await z());const a=this._container.scrollHeight;this._container.style.height=`${a}px`,i||setTimeout((()=>{this._container.style.height="0px"}),0),this.expanded=i,l(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host {
        display: block;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        border-radius: var(--ha-card-border-radius, 4px);
      }

      #summary {
        display: flex;
        padding: var(--expansion-panel-summary-padding, 0 8px);
        min-height: 48px;
        align-items: center;
        cursor: pointer;
        overflow: hidden;
        font-weight: 500;
        outline: none;
      }

      #summary:focus {
        background: var(--input-fill-color);
      }

      .summary-icon {
        transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
        margin-left: auto;
      }

      .summary-icon.expanded {
        transform: rotate(180deg);
      }

      .container {
        padding: var(--expansion-panel-content-padding, 0 8px);
        overflow: hidden;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
        height: 0px;
      }

      .container.expanded {
        height: auto;
      }

      .header {
        display: block;
      }

      .secondary {
        display: block;
        color: var(--secondary-text-color);
        font-size: 12px;
      }
    `}}]}}),i);let N=e([c("vais-update-dialog")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[a()],key:"repository",value:void 0},{kind:"field",decorators:[a({type:Boolean})],key:"_updating",value:()=>!1},{kind:"field",decorators:[a()],key:"_error",value:void 0},{kind:"field",decorators:[a({attribute:!1})],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>p(((e,i)=>e.find((e=>e.id===i))))},{kind:"method",key:"firstUpdated",value:async function(e){m(v(t.prototype),"firstUpdated",this).call(this,e);const i=this._getRepository(this.vais.repositories,this.repository);i&&("commit"!==i.version_or_commit&&(this._releaseNotes=await u(this.hass,i.id),this._releaseNotes=this._releaseNotes.filter((e=>e.tag>i.installed_version))),g(this.hass,(e=>this._error=e),y.ERROR))}},{kind:"method",key:"render",value:function(){var e;if(!this.active)return o``;const i=this._getRepository(this.vais.repositories,this.repository);return i?o`
      <vais-dialog
        .active=${this.active}
        .title=${this.vais.localize("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${r({content:!0,narrow:this.narrow})}>
          <p class="message">
            ${this.vais.localize("dialog_update.message",{name:i.name})}
          </p>
          <div class="version-container">
            <div class="version-element">
              <span class="version-number">${i.installed_version}</span>
              <small class="version-text">${this.vais.localize("dialog_update.downloaded_version")}</small>
            </div>

            <span class="version-separator">
              <ha-svg-icon
                .path=${f}
              ></ha-svg-icon>
            </span>

            <div class="version-element">
                <span class="version-number">${i.avaislable_version}</span>
                <small class="version-text">${this.vais.localize("dialog_update.avaislable_version")}</small>
              </div>
            </div>
          </div>

          ${this._releaseNotes.length>0?this._releaseNotes.map((e=>o`
                    <ha-expansion-panel
                      .header=${e.name&&e.name!==e.tag?`${e.tag}: ${e.name}`:e.tag}
                      outlined
                      ?expanded=${1===this._releaseNotes.length}
                    >
                      ${e.body?R.html(e.body,i):this.vais.localize("dialog_update.no_info")}
                    </ha-expansion-panel>
                  `)):""}
          ${i.can_install?"":o`<ha-alert alert-type="error" .rtl=${w(this.hass)}>
                  ${this.vais.localize("confirm.home_assistant_version_not_correct",{haversion:this.hass.config.version,minversion:i.homeassistant})}
                </ha-alert>`}
          ${"integration"===i.category?o`<p>${this.vais.localize("dialog_download.restart")}</p>`:""}
          ${null!==(e=this._error)&&void 0!==e&&e.message?o`<ha-alert alert-type="error" .rtl=${w(this.hass)}>
                  ${this._error.message}
                </ha-alert>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!i.can_install}
          @click=${this._updateRepository}
          raised
          >
          ${this._updating?o`<ha-circular-progress active size="small"></ha-circular-progress>`:this.vais.localize("common.update")}
          </mwc-button
        >
        <div class="secondary" slot="secondaryaction">
          <vais-link .url=${this._getChanglogURL()||""}>
            <mwc-button>${this.vais.localize("dialog_update.changelog")}
          </mwc-button>
          </vais-link>
          <vais-link .url="https://github.com/${i.full_name}">
            <mwc-button>${this.vais.localize("common.repository")}
          </mwc-button>
          </vais-link>
        </div>
      </vais-dialog>
    `:o``}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const e=this._getRepository(this.vais.repositories,this.repository);e&&("commit"!==e.version_or_commit?await x(this.hass,e.id,e.avaislable_version):await _(this.hass,e.id),"plugin"===e.category&&"storage"===this.vais.status.lovelace_mode&&await C(this.hass,e,e.avaislable_version),this._updating=!1,this.dispatchEvent(new Event("vais-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===e.category&&j(this,{title:this.vais.localize("common.reload"),text:o`${this.vais.localize("dialog.reload.description")}<br />${this.vais.localize("dialog.reload.confirm")}`,dismissText:this.vais.localize("common.cancel"),confirmText:this.vais.localize("common.reload"),confirm:()=>{k.location.href=k.location.href}}))}},{kind:"method",key:"_getChanglogURL",value:function(){const e=this._getRepository(this.vais.repositories,this.repository);if(e)return"commit"===e.version_or_commit?`https://github.com/${e.full_name}/compare/${e.installed_version}...${e.avaislable_version}`:`https://github.com/${e.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[b,$,d`
        .content {
          width: 360px;
          display: contents;
        }
        ha-expansion-panel {
          margin: 8px 0;
        }
        ha-expansion-panel[expanded] {
          padding-bottom: 16px;
        }

        .secondary {
          display: flex;
        }
        .message {
          text-align: center;
          margin: 0;
        }
        .version-container {
          margin: 24px 0 12px 0;
          width: 360px;
          min-width: 100%;
          max-width: 100%;
          display: flex;
          flex-direction: row;
        }
        .version-element {
          display: flex;
          flex-direction: column;
          flex: 1;
          padding: 0 12px;
          text-align: center;
        }
        .version-text {
          color: var(--secondary-text-color);
        }
        .version-number {
          font-size: 1.5rem;
          margin-bottom: 4px;
        }
      `]}}]}}),h);export{N as VaisUpdateDialog};
