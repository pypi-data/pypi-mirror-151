import{a as o,V as s,e as t,t as i,$ as e,W as a,X as r,Y as c,Z as d,a0 as n,a1 as l,s as h,d as p,r as m,n as v}from"./main-e088bb19.js";import{a as u}from"./c.166c4b5c.js";import"./c.e9faf9fb.js";import"./c.efa39a97.js";import"./c.3b8f3ca0.js";import"./c.14628ea3.js";import"./c.0bdb0337.js";import"./c.8e28b461.js";import"./c.44ff3154.js";import"./c.06c5e585.js";import"./c.c8c7ce92.js";import"./c.7312bad4.js";import"./c.2b12d4b5.js";import"./c.2ef5c8dd.js";import"./c.ceb1e431.js";import"./c.7943fa91.js";let g=o([v("vais-custom-repositories-dialog")],(function(o,s){return{F:class extends s{constructor(...s){super(...s),o(this)}},d:[{kind:"field",decorators:[t()],key:"_error",value:void 0},{kind:"field",decorators:[i()],key:"_progress",value:()=>!1},{kind:"field",decorators:[i()],key:"_addRepositoryData",value:()=>({category:void 0,repository:void 0})},{kind:"field",decorators:[i()],key:"_customRepositories",value:void 0},{kind:"method",key:"shouldUpdate",value:function(o){return o.has("narrow")||o.has("active")||o.has("_error")||o.has("_addRepositoryData")||o.has("_customRepositories")||o.has("_progress")}},{kind:"method",key:"render",value:function(){var o,s;if(!this.active)return e``;const t=[{name:"repository",selector:{text:{}}},{name:"category",selector:{select:{mode:"dropdown",options:this.vais.configuration.categories.map((o=>({value:o,label:this.vais.localize(`common.${o}`)})))}}}];return e`
      <vais-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.vais.localize("dialog_custom_repositories.title")}
        scrimClickAction
        escapeKeyAction
        maxWidth
      >
        <div class="content">
          <div class="list" ?narrow=${this.narrow}>
            ${null!==(o=this._error)&&void 0!==o&&o.message?e`<ha-alert alert-type="error" .rtl=${u(this.hass)}>
                  ${this._error.message}
                </ha-alert>`:""}
            ${null===(s=this._customRepositories)||void 0===s?void 0:s.filter((o=>this.vais.configuration.categories.includes(o.category))).map((o=>e`<ha-settings-row
                  @click=${()=>this._showReopsitoryInfo(String(o.id))}
                >
                  <span slot="heading">${o.name}</span>
                  <span slot="description">${o.full_name} (${o.category})</span>

                  <mwc-icon-button
                    @click=${s=>{s.stopPropagation(),this._removeRepository(o.id)}}
                  >
                    <ha-svg-icon class="delete" .path=${a}></ha-svg-icon>
                  </mwc-icon-button>
                </ha-settings-row>`))}
          </div>
          <ha-form
            ?narrow=${this.narrow}
            .data=${this._addRepositoryData}
            .schema=${t}
            .computeLabel=${o=>"category"===o.name?this.vais.localize("dialog_custom_repositories.category"):this.vais.localize("common.repository")}
            @value-changed=${this._valueChanged}
          >
          </ha-form>
        </div>
        <mwc-button
          slot="primaryaction"
          raised
          .disabled=${void 0===this._addRepositoryData.category||void 0===this._addRepositoryData.repository}
          @click=${this._addRepository}
        >
          ${this._progress?e`<ha-circular-progress active size="small"></ha-circular-progress>`:this.vais.localize("common.add")}
        </mwc-button>
      </vais-dialog>
    `}},{kind:"method",key:"firstUpdated",value:function(){var o;r(this.hass,(o=>this._error=o),c.ERROR),this._customRepositories=null===(o=this.vais.repositories)||void 0===o?void 0:o.filter((o=>o.custom))}},{kind:"method",key:"_valueChanged",value:function(o){this._addRepositoryData=o.detail.value}},{kind:"method",key:"_addRepository",value:async function(){if(this._error=void 0,this._progress=!0,!this._addRepositoryData.category)return void(this._error={message:this.vais.localize("dialog_custom_repositories.no_category")});if(!this._addRepositoryData.repository)return void(this._error={message:this.vais.localize("dialog_custom_repositories.no_repository")});await d(this.hass,this._addRepositoryData.repository,this._addRepositoryData.category);const o=await n(this.hass);this.dispatchEvent(new CustomEvent("update-vais",{detail:{repositories:o},bubbles:!0,composed:!0})),this._customRepositories=o.filter((o=>o.custom)),this._progress=!1}},{kind:"method",key:"_removeRepository",value:async function(o){this._error=void 0,await l(this.hass,o);const s=await n(this.hass);this.dispatchEvent(new CustomEvent("update-vais",{detail:{repositories:s},bubbles:!0,composed:!0})),this._customRepositories=s.filter((o=>o.custom))}},{kind:"method",key:"_showReopsitoryInfo",value:async function(o){this.dispatchEvent(new CustomEvent("vais-dialog-secondary",{detail:{type:"repository-info",repository:o},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[h,p,m`
        .list {
          position: relative;
          max-height: calc(100vh - 500px);
          overflow: auto;
        }
        ha-form {
          display: block;
          padding: 25px 0;
        }
        ha-form[narrow] {
          background-color: var(--card-background-color);
          bottom: 0;
          position: absolute;
          width: calc(100% - 48px);
        }
        ha-svg-icon {
          --mdc-icon-size: 36px;
        }
        ha-svg-icon:not(.delete) {
          margin-right: 4px;
        }
        ha-settings-row {
          cursor: pointer;
          padding: 0;
        }
        .list[narrow] > ha-settings-row:last-of-type {
          margin-bottom: 162px;
        }
        .delete {
          color: var(--hcv-color-error);
        }

        @media all and (max-width: 450px), all and (max-height: 500px) {
          .list {
            max-height: calc(100vh - 162px);
          }
        }
      `]}}]}}),s);export{g as VaisCustomRepositoriesDialog};
