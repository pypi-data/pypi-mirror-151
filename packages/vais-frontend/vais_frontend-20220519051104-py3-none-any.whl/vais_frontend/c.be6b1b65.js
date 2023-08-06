import{_ as i,n as e,a as t,V as s,e as a,b as r,m as o,$ as l,o as n,c as d,s as c,d as h,r as p}from"./main-e088bb19.js";import{f as u}from"./c.d2a4fbfa.js";import"./c.0bdb0337.js";import{s as v,S as f,a as m}from"./c.7312bad4.js";import"./c.2ef5c8dd.js";import"./c.3b8f3ca0.js";import{b as g}from"./c.fcc8c8a6.js";import"./c.14628ea3.js";import"./c.44ff3154.js";import"./c.8e28b461.js";import"./c.ceb1e431.js";import"./c.7943fa91.js";import"./c.166c4b5c.js";let y=class extends f{};y.styles=[v],y=i([e("mwc-select")],y);const _=["stars","last_updated","name"];let k=t([e("vais-add-repository-dialog")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[a({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[a({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[a()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[a()],key:"_sortBy",value:()=>_[0]},{kind:"field",decorators:[a()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(i){return i.forEach(((i,e)=>{"hass"===e&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))})),i.has("narrow")||i.has("filters")||i.has("active")||i.has("_searchInput")||i.has("_load")||i.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(i,e)=>null==i?void 0:i.filter((i=>{var t,s;return!i.installed&&(null===(t=this.vais.sections)||void 0===t||null===(s=t.find((i=>i.id===this.section)).categories)||void 0===s?void 0:s.includes(i.category))&&!i.installed&&(null==e?void 0:e.includes(i.category))}))}},{kind:"method",key:"firstUpdated",value:async function(){var i;if(this.addEventListener("filter-change",(i=>this._updateFilters(i))),0===(null===(i=this.filters)||void 0===i?void 0:i.length)){var e;const i=null===(e=r(this.vais.language,this.route))||void 0===e?void 0:e.categories;null==i||i.filter((i=>{var e;return null===(e=this.vais.configuration)||void 0===e?void 0:e.categories.includes(i)})).forEach((i=>{this.filters.push({id:i,value:i,checked:!0})})),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(i){const e=this.filters.find((e=>e.id===i.detail.id));this.filters.find((i=>i.id===e.id)).checked=!e.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>o(u)},{kind:"method",key:"render",value:function(){var i;if(!this.active)return l``;this._searchInput=window.localStorage.getItem("vais-search")||"";let e=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(i=this.vais.configuration)||void 0===i?void 0:i.categories),this._searchInput);return 0!==this.filters.length&&(e=e.filter((i=>{var e;return null===(e=this.filters.find((e=>e.id===i.category)))||void 0===e?void 0:e.checked}))),l`
      <vais-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.vais.localize("dialog_add_repo.title")}
        hideActions
        scrimClickAction
        maxWidth
      >
        <div class="searchandfilter" ?narrow=${this.narrow}>
          <search-input
            .hass=${this.hass}
            .label=${this.vais.localize("search.placeholder")}
            .filter=${this._searchInput}
            @value-changed=${this._inputValueChanged}
            ?narrow=${this.narrow}
          ></search-input>
          <mwc-select
            ?narrow=${this.narrow}
            .label=${this.vais.localize("dialog_add_repo.sort_by")}
            .value=${this._sortBy}
            @selected=${i=>this._sortBy=i.currentTarget.value}
            @closed=${m}
          >
            ${_.map((i=>l`<mwc-list-item .value=${i}>
                  ${this.vais.localize(`dialog_add_repo.sort_by_values.${i}`)||i}
                </mwc-list-item>`))}
          </mwc-select>
        </div>
        ${this.filters.length>1?l`<div class="filters">
              <vais-filter .vais=${this.vais} .filters="${this.filters}"></vais-filter>
            </div>`:""}
        <div class=${n({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${n({list:!0,narrow:this.narrow})}>
            ${e.sort(((i,e)=>"name"===this._sortBy?i.name.toLocaleLowerCase()<e.name.toLocaleLowerCase()?-1:1:i[this._sortBy]>e[this._sortBy]?-1:1)).slice(0,this._load).map((i=>l` <ha-settings-row
                  class=${n({narrow:this.narrow})}
                  @click=${()=>this._openInformation(i)}
                >
                  ${this.narrow?"":"integration"===i.category?l`
                          <img
                            slot="prefix"
                            loading="lazy"
                            .src=${g({domain:i.domain,darkOptimized:this.hass.themes.darkMode,type:"icon"})}
                            referrerpolicy="no-referrer"
                            @error=${this._onImageError}
                            @load=${this._onImageLoad}
                          />
                        `:""}
                  <span slot="heading"> ${i.name} </span>
                  <span slot="description">${i.description}</span>
                  ${"integration"!==i.category?l`<ha-chip>${this.vais.localize(`common.${i.category}`)}</ha-chip> `:""}
                </ha-settings-row>`))}
            ${0===e.length?l`<p>${this.vais.localize("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </vais-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(i){const e=i.target.scrollTop;e>=this._top?this._load+=1:this._load-=1,this._top=e}},{kind:"method",key:"_inputValueChanged",value:function(i){this._searchInput=i.detail.value,window.localStorage.setItem("vais-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(i){this.dispatchEvent(new CustomEvent("vais-dialog-secondary",{detail:{type:"repository-info",repository:i.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(i){i.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(i){var e;if(null!==(e=i.target)&&void 0!==e&&e.outerHTML)try{i.target.outerHTML=`<ha-svg-icon path="${d}" slot="prefix"></ha-svg-icon>`}catch(i){}}},{kind:"get",static:!0,key:"styles",value:function(){return[c,h,p`
        .content {
          width: 100%;
          overflow: auto;
          max-height: 70vh;
        }

        .filter {
          margin-top: -12px;
          display: flex;
          width: 200px;
          float: right;
        }

        .list {
          margin-top: 16px;
          width: 1024px;
          max-width: 100%;
        }
        ha-svg-icon {
          --mdc-icon-size: 36px;
          margin-right: 6px;
        }
        search-input {
          display: block;
          float: left;
          width: 75%;
        }
        search-input[narrow],
        mwc-select[narrow] {
          width: 100%;
          margin: 4px 0;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-right: 6px;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
        }

        .filters {
          width: 100%;
          display: flex;
        }

        vais-filter {
          width: 100%;
          margin-left: -32px;
        }

        ha-settings-row {
          padding: 0px 16px 0 0;
          cursor: pointer;
        }

        .searchandfilter {
          display: flex;
          justify-content: space-between;
          align-items: self-end;
        }

        .searchandfilter[narrow] {
          flex-direction: column;
        }
      `]}}]}}),s);export{k as VaisAddRepositoryDialog};
