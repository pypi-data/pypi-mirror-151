import{a as i,V as s,e as o,t,m as e,ah as a,a0 as r,X as l,Y as n,$ as d,ai as h,aj as c,ak as p,al as _,am as v,ag as y,d as m,r as u,n as g}from"./main-e088bb19.js";import{a as f}from"./c.166c4b5c.js";import"./c.e9faf9fb.js";import"./c.efa39a97.js";import{s as b}from"./c.d8002660.js";import{u as w}from"./c.e60bf0f8.js";import"./c.3c6412dd.js";import"./c.14628ea3.js";import"./c.0bdb0337.js";import"./c.8e28b461.js";import"./c.44ff3154.js";import"./c.06c5e585.js";import"./c.c8c7ce92.js";import"./c.7312bad4.js";import"./c.2b12d4b5.js";import"./c.2ef5c8dd.js";import"./c.7943fa91.js";let k=i([g("vais-download-dialog")],(function(i,s){return{F:class extends s{constructor(...s){super(...s),i(this)}},d:[{kind:"field",decorators:[o()],key:"repository",value:void 0},{kind:"field",decorators:[t()],key:"_toggle",value:()=>!0},{kind:"field",decorators:[t()],key:"_installing",value:()=>!1},{kind:"field",decorators:[t()],key:"_error",value:void 0},{kind:"field",decorators:[t()],key:"_repository",value:void 0},{kind:"field",decorators:[t()],key:"_downloadRepositoryData",value:()=>({beta:!1,version:""})},{kind:"method",key:"shouldUpdate",value:function(i){return i.forEach(((i,s)=>{"hass"===s&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===s&&(this._repository=this._getRepository(this.vais.repositories,this.repository))})),i.has("sidebarDocked")||i.has("narrow")||i.has("active")||i.has("_toggle")||i.has("_error")||i.has("_repository")||i.has("_downloadRepositoryData")||i.has("_installing")}},{kind:"field",key:"_getRepository",value:()=>e(((i,s)=>null==i?void 0:i.find((i=>i.id===s))))},{kind:"field",key:"_getInstallPath",value:()=>e((i=>{let s=i.local_path;return"theme"===i.category&&(s=`${s}/${i.file_name}`),s}))},{kind:"method",key:"firstUpdated",value:async function(){var i,s;if(this._repository=this._getRepository(this.vais.repositories,this.repository),null===(i=this._repository)||void 0===i||!i.updated_info){await a(this.hass,this._repository.id);const i=await r(this.hass);this.dispatchEvent(new CustomEvent("update-vais",{detail:{repositories:i},bubbles:!0,composed:!0})),this._repository=this._getRepository(i,this.repository)}this._toggle=!1,l(this.hass,(i=>this._error=i),n.ERROR),this._downloadRepositoryData.beta=this._repository.beta,this._downloadRepositoryData.version="version"===(null===(s=this._repository)||void 0===s?void 0:s.version_or_commit)?this._repository.releases[0]:""}},{kind:"method",key:"render",value:function(){var i;if(!this.active||!this._repository)return d``;const s=this._getInstallPath(this._repository),o=[{name:"beta",selector:{boolean:{}}},{name:"version",selector:{select:{options:"version"===this._repository.version_or_commit?this._repository.releases.concat("vais/integration"===this._repository.full_name||this._repository.hide_default_branch?[]:[this._repository.default_branch]):[],mode:"dropdown"}}}];return d`
      <vais-dialog
        .active=${this.active}
        .narrow=${this.narrow}
        .hass=${this.hass}
        .secondary=${this.secondary}
        .title=${this._repository.name}
      >
        <div class="content">
          ${"version"===this._repository.version_or_commit?d`
                <ha-form
                  .disabled=${this._toggle}
                  ?narrow=${this.narrow}
                  .data=${this._downloadRepositoryData}
                  .schema=${o}
                  .computeLabel=${i=>"beta"===i.name?this.vais.localize("dialog_download.show_beta"):this.vais.localize("dialog_download.select_version")}
                  @value-changed=${this._valueChanged}
                >
                </ha-form>
              `:""}
          ${this._repository.can_install?"":d`<ha-alert alert-type="error" .rtl=${f(this.hass)}>
                ${this.vais.localize("confirm.home_assistant_version_not_correct",{haversion:this.hass.config.version,minversion:this._repository.homeassistant})}
              </ha-alert>`}
          <div class="note">
            ${this.vais.localize("dialog_download.note_downloaded",{location:d`<code>'${s}'</code>`})}
            ${"plugin"===this._repository.category&&"storage"!==this.vais.status.lovelace_mode?d`
                  <p>${this.vais.localize("dialog_download.lovelace_instruction")}</p>
                  <pre>
                url: ${h({repository:this._repository,skipTag:!0})}
                type: module
                </pre
                  >
                `:""}
            ${"integration"===this._repository.category?d`<p>${this.vais.localize("dialog_download.restart")}</p>`:""}
          </div>
          ${null!==(i=this._error)&&void 0!==i&&i.message?d`<ha-alert alert-type="error" .rtl=${f(this.hass)}>
                ${this._error.message}
              </ha-alert>`:""}
        </div>
        <mwc-button
          raised
          slot="primaryaction"
          ?disabled=${!(this._repository.can_install&&!this._toggle&&"version"!==this._repository.version_or_commit)&&!this._downloadRepositoryData.version}
          @click=${this._installRepository}
        >
          ${this._installing?d`<ha-circular-progress active size="small"></ha-circular-progress>`:this.vais.localize("common.download")}
        </mwc-button>
        <vais-link slot="secondaryaction" .url="https://github.com/${this._repository.full_name}">
          <mwc-button> ${this.vais.localize("common.repository")} </mwc-button>
        </vais-link>
      </vais-dialog>
    `}},{kind:"method",key:"_valueChanged",value:async function(i){let s=!1;if(this._downloadRepositoryData.beta!==i.detail.value.beta&&(s=!0,this._toggle=!0,await c(this.hass,this.repository)),i.detail.value.version&&(s=!0,this._toggle=!0,await p(this.hass,this.repository,i.detail.value.version)),s){const i=await r(this.hass);this.dispatchEvent(new CustomEvent("update-vais",{detail:{repositories:i},bubbles:!0,composed:!0})),this._repository=this._getRepository(i,this.repository),this._toggle=!1}this._downloadRepositoryData=i.detail.value}},{kind:"method",key:"_installRepository",value:async function(){var i;if(this._installing=!0,!this._repository)return;const s=this._downloadRepositoryData.version||this._repository.avaislable_version||this._repository.default_branch;"commit"!==(null===(i=this._repository)||void 0===i?void 0:i.version_or_commit)?await _(this.hass,this._repository.id,s):await v(this.hass,this._repository.id),this.vais.log.debug(this._repository.category,"_installRepository"),this.vais.log.debug(this.vais.status.lovelace_mode,"_installRepository"),"plugin"===this._repository.category&&"storage"===this.vais.status.lovelace_mode&&await w(this.hass,this._repository,s),this._installing=!1,this.dispatchEvent(new Event("vais-secondary-dialog-closed",{bubbles:!0,composed:!0})),this.dispatchEvent(new Event("vais-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===this._repository.category&&b(this,{title:this.vais.localize("common.reload"),text:d`${this.vais.localize("dialog.reload.description")}<br />${this.vais.localize("dialog.reload.confirm")}`,dismissText:this.vais.localize("common.cancel"),confirmText:this.vais.localize("common.reload"),confirm:()=>{y.location.href=y.location.href}})}},{kind:"get",static:!0,key:"styles",value:function(){return[m,u`
        .note {
          margin-top: 12px;
        }
        .lovelace {
          margin-top: 8px;
        }
        pre {
          white-space: pre-line;
          user-select: all;
        }
      `]}}]}}),s);export{k as VaisDonwloadDialog};
