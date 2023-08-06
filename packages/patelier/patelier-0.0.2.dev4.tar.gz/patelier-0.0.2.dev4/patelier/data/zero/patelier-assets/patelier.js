const OK = "OK";
const ACT = "act";
const INACT = "inact";
const ACTMENU = "actmenu";
const NAV_SRC = "navSrc";
const NAV_WARN = "navWarn";
const NAV_CL = "navCl";
const NAV_CLEL = "navClEl";
const NAV_TR = "navTr";
const NAV_TREL = "navTrEl";
const NAV_SPC = "navSpc";
const NAV_SPCHD = "navSpcHd";
const NAV_SPCCL = "navSpcCl";
const NAV_ABS = "navAbs";
const NAV_FIG = "navFig";
const NAV_REF = "navRef";
const NAV_WD = "navWd";
const NAV_WDLIST = "navWdList";
const ART_SRC = "artSrc";
const ART_WARN = "artWarn";
const ART_CL = "artCl";
const ART_CLEL = "artClEl";
const ART_TR = "artTr";
const ART_SPC = "artSpc";
const ART_SPCHD = "artSpcHd";
const ART_SPCCL = "artSpcCl";
const ART_ABS = "artAbs";
const ART_FIG = "artFig";
const ART_REF = "artRef";
const ART_WD = "artWd";
const ART_WDLIST = "artWdList";
const BRIGHT = "bright";
const DARK = "dark";
const SCT_SRC = "sctSrc";
const SCT_WARN = "sctWarn";
const SCT_CL = "sctCl";
const SCT_CLEL = "sctClEl";
const SCT_TR = "sctTr";
const SCT_SPC = "sctSpc";
const SCT_SPCHD = "sctSpcHd";
const SCT_SPCCL = "sctSpcCl";
const SCT_ABS = "sctAbs";
const SCT_FIG = "sctFig";
const SCT_REF = "sctRef";
const SCT_WD = "sctWd";
const SCT_WDLIST = "sctWdList";
const LIST_SWITCH = "list-switch";
const ACTLIST = "actlist";
const H_ACTLIST = "hactlist";
const V_ACTLIST = "vactlist";
const INACTLIST = "inactlist";
const ACTCPY = "actcpy";
const INACTCPY = "inactcpy";
const ACTPRN = "actprn";
const INACTPRN = "inactprn";
const CP_CL_JPLIST = "cpyFclJpList";
const CP_CL_JELIST = "cpyFclJEList";
const CP_CLEL_LIST = "cpyFclElList";
const CP_TR_LIST = "cpyFtrList";
const CP_TREL_LIST = "cpyFtrElList";
const CP_SPC_JPLIST = "cpyFspcJpList";
const CP_SPC_JELIST = "cpyFspcJEList";
const CP_SPCHD_LIST = "cpyFspcHdList";
const CP_SPCHDPARA_LIST = "cpyFspcHdParaList";
const CP_SPCCL_LIST = "cpyFspcClList";
const CP_ABS_JPLIST = "cpyFabsJpList";
const CP_ABS_PCTLIST = "cpyFabsPctList";
const CP_FIG_LIST = "cpyFfigList";
const PRN_SVGFIG_LIST = "prnsvgfigList";
const CP_REF_CLLIST1 = "cpyFrefClList1";
const CP_REF_CLLIST2 = "cpyFrefClList2";
const CP_REF_EBLIST1 = "cpyFrefEbList1";
const CP_REF_EBLIST2 = "cpyFrefEbList2";
const CP_WD_CLLIST1 = "cpyFwdClList1";
const CP_WD_CLLIST2 = "cpyFwdClList2";
const CP_WD_EBLIST1 = "cpyFwdEbList1";
const CP_WD_EBLIST2 = "cpyFwdEbList2";
const CP_WDLIST_LIST = "cpyFwdList";
const CL_JPLIST = "clJpList";
const CL_JELIST = "clJEList";
const CLEL_LIST = "clElList";
const TR_LIST = "trList";
const TREL_LIST = "trElList";
const SPC_JPLIST = "spcJpList";
const SPC_JELIST = "spcJEList";
const SPCHD_LIST = "spcHdList";
const SPCHDPARA_LIST = "spcHdParaList";
const SPCCL_LIST = "spcClList";
const ABS_JPLIST = "absJpList";
const ABS_PCTLIST = "absPctList";
const FIG_LIST = "figList";
const SVGFIG_LIST = "svgfigList";
const REF_CLLIST1 = "refClList1";
const REF_CLLIST2 = "refClList2";
const REF_EBLIST1 = "refEbList1";
const REF_EBLIST2 = "refEbList2";
const WD_CLLIST1 = "wdClList1";
const WD_CLLIST2 = "wdClList2";
const WD_EBLIST1 = "wdEbList1";
const WD_EBLIST2 = "wdEbList2";
const WDLIST_LIST = "wdList";
const GRPH_SC = "grphSc";
const CL_ABBR = "clabbr";

function tip(spanElement){
  if (spanElement){
    const tmpWordIdList = spanElement.className.split(' ');
    let wdId = tmpWordIdList[0];
    if ('k' == wdId || 'w' == wdId){
      wdId = tmpWordIdList[1];
    }
    if (wdId in ARRAY_TIP){
      spanElement.title = ARRAY_TIP[wdId];
    }
  }
}

function clListRst(){
  let listElement = document.getElementById(CL_JPLIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_CL_JPLIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(CL_JELIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_CL_JELIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function cl1stListOpn(){
  let listElement = document.getElementById(CL_JELIST);
  if (listElement){
    if (INACTLIST == listElement.className){
      listElement = document.getElementById(CL_JPLIST);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement.className = ACTLIST;
          listElement = document.getElementById(CP_CL_JPLIST);
          if (listElement){
            if (ACTCPY != listElement.className){
              listElement.className = ACTCPY;
            }
          }
        }
      }
    }
  } else {
    listElement = document.getElementById(CL_JPLIST);
    if (listElement){
      if (ACTLIST != listElement.className){
        listElement.className = ACTLIST;
        listElement = document.getElementById(CP_CL_JPLIST);
        if (listElement){
          if (ACTCPY != listElement.className){
            listElement.className = ACTCPY;
          }
        }
      }
    }
  }
}

function clElListRst(){
  let listElement = document.getElementById(CLEL_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_CLEL_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function clEl1stListOpn(){
  let listElement = document.getElementById(CLEL_LIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_CLEL_LIST);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
}

function trListRst(){
  let listElement = document.getElementById(TR_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_TR_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(TREL_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_TREL_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function tr1stListOpn(){
  let listElement = document.getElementById(TREL_LIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement = document.getElementById(TR_LIST);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement.className = ACTLIST;
          listElement = document.getElementById(CP_TR_LIST);
          if (listElement){
            if (ACTCPY != listElement.className){
              listElement.className = ACTCPY;
            }
          }
        }
      }
    }
  }
}

function spcListRst(){
  let listElement = document.getElementById(SPC_JPLIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPC_JPLIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(SPC_JELIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPC_JELIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function spc1stListOpn(){
  let listElement = document.getElementById(SPC_JELIST);
  if (listElement){
    if (INACTLIST == listElement.className){
      listElement = document.getElementById(SPC_JPLIST);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement.className = ACTLIST;
          listElement = document.getElementById(CP_SPC_JPLIST);
          if (listElement){
            if (ACTCPY != listElement.className){
              listElement.className = ACTCPY;
            }
          }
        }
      }
    }
  } else {
    listElement = document.getElementById(SPC_JPLIST);
    if (listElement){
      if (ACTLIST != listElement.className){
        listElement.className = ACTLIST;
        listElement = document.getElementById(CP_SPC_JPLIST);
        if (listElement){
          if (ACTCPY != listElement.className){
            listElement.className = ACTCPY;
          }
        }
      }
    }
  }
}

function spcHdListRst(){
  let listElement = document.getElementById(SPCHD_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPCHD_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(SPCHDPARA_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPCHDPARA_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function spcHd1stListOpn(){
  let listElement = document.getElementById(SPCHDPARA_LIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement = document.getElementById(SPCHD_LIST);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement.className = ACTLIST;
          listElement = document.getElementById(CP_SPCHD_LIST);
          if (listElement){
            if (ACTCPY != listElement.className){
              listElement.className = ACTCPY;
            }
          }
        }
      }
    }
  } else {
    listElement = document.getElementById(SPCHD_LIST);
    if (listElement){
      if (ACTLIST != listElement.className){
        listElement.className = ACTLIST;
        listElement = document.getElementById(CP_SPCHD_LIST);
        if (listElement){
          if (ACTCPY != listElement.className){
            listElement.className = ACTCPY;
          }
        }
      }
    }
  }
}

function spcClListRst(){
  let listElement = document.getElementById(SPCCL_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPCCL_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function spcCl1stListOpn(){
  let listElement = document.getElementById(SPCCL_LIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_SPCCL_LIST);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
}

function absListRst(){
  let listElement = document.getElementById(ABS_JPLIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_ABS_JPLIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(ABS_PCTLIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_ABS_PCTLIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function abs1stListOpn(){
  let listElement = document.getElementById(ABS_PCTLIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement = document.getElementById(ABS_JPLIST);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement.className = ACTLIST;
          listElement = document.getElementById(CP_ABS_JPLIST);
          if (listElement){
            if (ACTCPY != listElement.className){
              listElement.className = ACTCPY;
            }
          }
        }
      }
    }
  }
}

function figListRst(){
  let listElement = document.getElementById(FIG_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_FIG_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(SVGFIG_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(PRN_SVGFIG_LIST);
      if (listElement){
        if (INACTPRN != listElement.className){
          listElement.className = INACTPRN;
        }
      }
    }
  }
}

function fig1stListOpn(){
  let listElement = document.getElementById(SVGFIG_LIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement = document.getElementById(FIG_LIST);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement.className = ACTLIST;
          listElement = document.getElementById(CP_FIG_LIST);
          if (listElement){
            if (ACTCPY != listElement.className){
              listElement.className = ACTCPY;
            }
          }
        }
      }
    }
  }
}

function refListRst(){
  let listElement = document.getElementById(REF_CLLIST1);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_REF_CLLIST1);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(REF_CLLIST2);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_REF_CLLIST2);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(REF_EBLIST1);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_REF_EBLIST1);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(REF_EBLIST2);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_REF_EBLIST2);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function ref1stListOpn(){
  let listElement = document.getElementById(REF_EBLIST2);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement = document.getElementById(REF_EBLIST1);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement = document.getElementById(REF_CLLIST2);
          if (listElement){
            if (ACTLIST != listElement.className){
              listElement = document.getElementById(REF_CLLIST1);
              if (listElement){
                if (ACTLIST != listElement.className){
                  listElement.className = ACTLIST;
                  listElement = document.getElementById(CP_REF_CLLIST1);
                  if (listElement){
                    if (ACTCPY != listElement.className){
                      listElement.className = ACTCPY;
                    }
                  }
                }
              }
            }
          } else {
            listElement = document.getElementById(REF_CLLIST1);
            if (listElement){
              if (ACTLIST != listElement.className){
                listElement.className = ACTLIST;
                listElement = document.getElementById(CP_REF_CLLIST1);
                if (listElement){
                  if (ACTCPY != listElement.className){
                    listElement.className = ACTCPY;
                  }
                }
              }
            }
          }
        }
      } else {
        listElement = document.getElementById(REF_CLLIST1);
        if (listElement){
          if (ACTLIST != listElement.className){
            listElement.className = ACTLIST;
            listElement = document.getElementById(CP_REF_CLLIST1);
            if (listElement){
              if (ACTCPY != listElement.className){
                listElement.className = ACTCPY;
              }
            }
          }
        }
      }
    }
  } else {
    listElement = document.getElementById(REF_CLLIST1);
    if (listElement){
      if (ACTLIST != listElement.className){
        listElement.className = ACTLIST;
        listElement = document.getElementById(CP_REF_CLLIST1);
        if (listElement){
          if (ACTCPY != listElement.className){
            listElement.className = ACTCPY;
          }
        }
      }
    }
  }
}

function wdListRst(){
  let listElement = document.getElementById(WD_CLLIST1);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_WD_CLLIST1);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(WD_CLLIST2);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_WD_CLLIST2);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(WD_EBLIST1);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_WD_EBLIST1);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(WD_EBLIST2);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_WD_EBLIST2);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function wd1stListOpn(){
  let listElement = document.getElementById(WD_EBLIST2);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement = document.getElementById(WD_EBLIST1);
      if (listElement){
        if (ACTLIST != listElement.className){
          listElement = document.getElementById(WD_CLLIST2);
          if (listElement){
            if (ACTLIST != listElement.className){
              listElement = document.getElementById(WD_CLLIST1);
              if (listElement){
                if (ACTLIST != listElement.className){
                  listElement.className = ACTLIST;
                  listElement = document.getElementById(CP_WD_CLLIST1);
                  if (listElement){
                    if (ACTCPY != listElement.className){
                      listElement.className = ACTCPY;
                    }
                  }
                }
              }
            }
          } else {
            listElement = document.getElementById(WD_CLLIST1);
            if (listElement){
              if (ACTLIST != listElement.className){
                listElement.className = ACTLIST;
                listElement = document.getElementById(CP_WD_CLLIST1);
                if (listElement){
                  if (ACTCPY != listElement.className){
                    listElement.className = ACTCPY;
                  }
                }
              }
            }
          }
        }
      } else {
        listElement = document.getElementById(WD_CLLIST1);
        if (listElement){
          if (ACTLIST != listElement.className){
            listElement.className = ACTLIST;
            listElement = document.getElementById(CP_WD_CLLIST1);
            if (listElement){
              if (ACTCPY != listElement.className){
                listElement.className = ACTCPY;
              }
            }
          }
        }
      }
    }
  } else {
    listElement = document.getElementById(WD_CLLIST1);
    if (listElement){
      if (ACTLIST != listElement.className){
        listElement.className = ACTLIST;
        listElement = document.getElementById(CP_WD_CLLIST1);
        if (listElement){
          if (ACTCPY != listElement.className){
            listElement.className = ACTCPY;
          }
        }
      }
    }
  }
}

function wdListListRst(){
  let listElement = document.getElementById(WDLIST_LIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_WDLIST_LIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function wdList1stListOpn(){
  let listElement = document.getElementById(WDLIST_LIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_WDLIST_LIST);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
}

function inactivate(navId, artId){
  const navElement = document.getElementById(navId);
  if (navElement){
    if (ACTMENU == navElement.className){
      navElement.className = "";
      const artElement = document.getElementById(artId);
      artElement.className = INACT;
    }
  }
}

function activate(navId, artId){
  const navElement = document.getElementById(navId);
  if (navElement){
    navElement.className = ACTMENU;
    const artElement = document.getElementById(artId);
    artElement.className = ACT;
  }
}

function srcActivate(){
  const navElement = document.getElementById(NAV_SRC);
  if (navElement){
    if (ACTMENU == navElement.className){
      const artElement = document.getElementById(ART_SRC);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      activate(NAV_SRC, ART_SRC);
    }
  }
}

document.addEventListener('DOMContentLoaded', srcActivate, false);

function warnActivate(){
  const navElement = document.getElementById(NAV_WARN);
  if (navElement){
    if (ACTMENU == navElement.className){
      const artElement = document.getElementById(ART_WARN);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      activate(NAV_WARN, ART_WARN);
    }
  }
}

function clActivate(){
  const navElement = document.getElementById(NAV_CL);
  if (navElement){
    if (ACTMENU == navElement.className){
      clListRst();
      const artElement = document.getElementById(ART_CL);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      cl1stListOpn();
      activate(NAV_CL, ART_CL);
    }
  }
}

function clElActivate(){
  const navElement = document.getElementById(NAV_CLEL);
  if (navElement){
    if (ACTMENU == navElement.className){
      clElListRst();
      const artElement = document.getElementById(ART_CLEL);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      clEl1stListOpn();
      activate(NAV_CLEL, ART_CLEL);
    }
  }
}

function trActivate(){
  const navElement = document.getElementById(NAV_TR);
  if (navElement){
    if (ACTMENU == navElement.className){
      trListRst();
      const artElement = document.getElementById(ART_TR);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      tr1stListOpn();
      activate(NAV_TR, ART_TR);
    }
  }
}

function spcActivate(){
  const navElement = document.getElementById(NAV_SPC);
  if (navElement){
    if (ACTMENU == navElement.className){
      spcListRst();
      const artElement = document.getElementById(ART_SPC);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      spc1stListOpn();
      activate(NAV_SPC, ART_SPC);
    }
  }
}

function spcHdActivate(){
  const navElement = document.getElementById(NAV_SPCHD);
  if (navElement){
    if (ACTMENU == navElement.className){
      spcHdListRst();
      const artElement = document.getElementById(ART_SPCHD);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      spcHd1stListOpn();
      activate(NAV_SPCHD, ART_SPCHD);
    }
  }
}

function spcClActivate(){
  const navElement = document.getElementById(NAV_SPCCL);
  if (navElement){
    if (ACTMENU == navElement.className){
      spcClListRst();
      const artElement = document.getElementById(ART_SPCCL);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      spcCl1stListOpn();
      activate(NAV_SPCCL, ART_SPCCL);
    }
  }
}

function absActivate(){
  const navElement = document.getElementById(NAV_ABS);
  if (navElement){
    if (ACTMENU == navElement.className){
      absListRst();
      const artElement = document.getElementById(ART_ABS);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      abs1stListOpn();
      activate(NAV_ABS, ART_ABS);
    }
  }
}

function figActivate(){
  const navElement = document.getElementById(NAV_FIG);
  if (navElement){
    if (ACTMENU == navElement.className){
      figListRst();
      const artElement = document.getElementById(ART_FIG);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      fig1stListOpn();
      activate(NAV_FIG, ART_FIG);
    }
  }
}

function refActivate(){
  const navElement = document.getElementById(NAV_REF);
  if (navElement){
    if (ACTMENU == navElement.className){
      refListRst();
      const artElement = document.getElementById(ART_REF);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      ref1stListOpn();
      activate(NAV_REF, ART_REF);
    }
  }
}

function wdActivate(){
  const navElement = document.getElementById(NAV_WD);
  if (navElement){
    if (ACTMENU == navElement.className){
      wdListRst();
      const artElement = document.getElementById(ART_WD);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WDLIST, ART_WDLIST);
      wd1stListOpn();
      activate(NAV_WD, ART_WD);
    }
  }
}

function wdListActivate(){
  const navElement = document.getElementById(NAV_WDLIST);
  if (navElement){
    if (ACTMENU == navElement.className){
      wdListListRst();
      const artElement = document.getElementById(ART_WDLIST);
      artElement.scrollTop = 0;
    } else if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      wdList1stListOpn();
      activate(NAV_WDLIST, ART_WDLIST);
    }
  }
}

function clMainListActivate(){
  let listElement = document.getElementById(CL_JPLIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_CL_JPLIST);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(CL_JELIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_CL_JELIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function spcMainListActivate(){
  let listElement = document.getElementById(SPC_JPLIST);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_SPC_JPLIST);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(SPC_JELIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPC_JELIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function spcEfListActivate(){
  let listElement = document.getElementById(SPC_JELIST);
  if (listElement){
    if (INACTLIST == listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_SPC_JELIST);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(SPC_JPLIST);
  if (listElement){
    if (INACTLIST != listElement.className){
      listElement.className = INACTLIST;
      listElement = document.getElementById(CP_SPC_JPLIST);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function wdMainListActivate(){
  let listElement = document.getElementById(WD_CLLIST2);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_WD_CLLIST2);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
  listElement = document.getElementById(WD_EBLIST1);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(CP_WD_EBLIST1);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    }
  }
}

function src(targetId){
  let targetElement;
  let navElement;
  navElement = document.getElementById(NAV_SRC);
  if (navElement){
    if ("" == navElement.className){
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      activate(NAV_SRC, ART_SRC);
    }
    targetElement = document.getElementById(targetId);
    targetElement.scrollIntoView(
        {behavior: "smooth", block: "start", inline: "nearest"});
  }
}

function cl(targetId){
  const navElement = document.getElementById(NAV_CL);
  if (navElement){
    if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      activate(NAV_CL, ART_CL);
    }
    clMainListActivate();
    const targetElement = document.getElementById(targetId);
    targetElement.scrollIntoView(
        {behavior: "smooth", block: "start", inline: "nearest"});
  }
}

function spc(targetId){
  const navElement = document.getElementById(NAV_SPC);
  if (navElement){
    if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WD, ART_WD);
      inactivate(NAV_WDLIST, ART_WDLIST);
      activate(NAV_SPC, ART_SPC);
    }
    spcMainListActivate();
    const targetElement = document.getElementById(targetId);
    targetElement.scrollIntoView(
        {behavior: "smooth", block: "start", inline: "nearest"});
  }
}

function wd(targetId){
  const navElement = document.getElementById(NAV_WD);
  if (navElement){
    if ("" == navElement.className){
      inactivate(NAV_SRC, ART_SRC);
      inactivate(NAV_WARN, ART_WARN);
      inactivate(NAV_CL, ART_CL);
      inactivate(NAV_CLEL, ART_CLEL);
      inactivate(NAV_TR, ART_TR);
      inactivate(NAV_SPC, ART_SPC);
      inactivate(NAV_SPCHD, ART_SPCHD);
      inactivate(NAV_SPCCL, ART_SPCCL);
      inactivate(NAV_ABS, ART_ABS);
      inactivate(NAV_FIG, ART_FIG);
      inactivate(NAV_REF, ART_REF);
      inactivate(NAV_WDLIST, ART_WDLIST);
      activate(NAV_WD, ART_WD);
    }
    wdMainListActivate();
    const targetElement = document.getElementById(targetId);
    targetElement.scrollIntoView(
        {behavior: "smooth", block: "start", inline: "nearest"});
  }
}

function line(targetId){
  let lineElement;
  let navElement;
  if ('c' == targetId.charAt(0)) {
    navElement = document.getElementById(NAV_CL);
    if (navElement){
      if ("" == navElement.className){
        inactivate(NAV_SRC, ART_SRC);
        inactivate(NAV_WARN, ART_WARN);
        inactivate(NAV_CLEL, ART_CLEL);
        inactivate(NAV_TR, ART_TR);
        inactivate(NAV_SPC, ART_SPC);
        inactivate(NAV_SPCHD, ART_SPCHD);
        inactivate(NAV_SPCCL, ART_SPCCL);
        inactivate(NAV_ABS, ART_ABS);
        inactivate(NAV_FIG, ART_FIG);
        inactivate(NAV_REF, ART_REF);
        inactivate(NAV_WD, ART_WD);
        inactivate(NAV_WDLIST, ART_WDLIST);
        activate(NAV_CL, ART_CL);
      }
      clMainListActivate();
      lineElement = document.getElementById(targetId);
      lineElement.scrollIntoView(
          {behavior: "smooth", block: "start", inline: "nearest"});
    }
  } else if ('e' == targetId.charAt(0)){
    navElement = document.getElementById(NAV_SPC);
    if (navElement){
      if ("" == navElement.className){
        inactivate(NAV_SRC, ART_SRC);
        inactivate(NAV_WARN, ART_WARN);
        inactivate(NAV_CL, ART_CL);
        inactivate(NAV_CLEL, ART_CLEL);
        inactivate(NAV_TR, ART_TR);
        inactivate(NAV_SPCHD, ART_SPCHD);
        inactivate(NAV_SPCCL, ART_SPCCL);
        inactivate(NAV_ABS, ART_ABS);
        inactivate(NAV_FIG, ART_FIG);
        inactivate(NAV_REF, ART_REF);
        inactivate(NAV_WD, ART_WD);
        inactivate(NAV_WDLIST, ART_WDLIST);
        activate(NAV_SPC, ART_SPC);
      }
      spcEfListActivate();
      lineElement = document.getElementById(targetId);
      lineElement.scrollIntoView(
          {behavior: "smooth", block: "start", inline: "nearest"});
    }
  } else {
    navElement = document.getElementById(NAV_SPC);
    if (navElement){
      if ("" == navElement.className){
        inactivate(NAV_SRC, ART_SRC);
        inactivate(NAV_WARN, ART_WARN);
        inactivate(NAV_CL, ART_CL);
        inactivate(NAV_CLEL, ART_CLEL);
        inactivate(NAV_TR, ART_TR);
        inactivate(NAV_SPCHD, ART_SPCHD);
        inactivate(NAV_SPCCL, ART_SPCCL);
        inactivate(NAV_ABS, ART_ABS);
        inactivate(NAV_FIG, ART_FIG);
        inactivate(NAV_REF, ART_REF);
        inactivate(NAV_WD, ART_WD);
        inactivate(NAV_WDLIST, ART_WDLIST);
        activate(NAV_SPC, ART_SPC);
      }
      spcMainListActivate();
      lineElement = document.getElementById(targetId);
      lineElement.scrollIntoView(
          {behavior: "smooth", block: "start", inline: "nearest"});
    }
  }
}

function sctColorChg(sct_id){
  const sctElement = document.getElementById(sct_id);
  if (sctElement){
    if (BRIGHT == sctElement.className){
      sctElement.className = DARK;
    } else {
      sctElement.className = BRIGHT;
    }
  }
}

function chgColor(){
  showGrphSc();
  setTimeout(deleteGrphSc, 2500);
  sctColorChg(SCT_SRC);
  sctColorChg(SCT_WARN);
  sctColorChg(SCT_CL);
  sctColorChg(SCT_CLEL);
  sctColorChg(SCT_TR);
  sctColorChg(SCT_SPC);
  sctColorChg(SCT_SPCHD);
  sctColorChg(SCT_SPCCL);
  sctColorChg(SCT_ABS);
  sctColorChg(SCT_FIG);
  sctColorChg(SCT_REF);
  sctColorChg(SCT_WD);
  sctColorChg(SCT_WDLIST);
}

function showGrphSc(){
  const bdyObj = document.getElementsByTagName('body').item(0); 
  const rect = bdyObj.getBoundingClientRect();
  const cvsW = rect.width;
  const cvsH = rect.height;
  const cvs = document.createElement('canvas'); 
  cvs.setAttribute("width", cvsW.toString());
  cvs.setAttribute("height", cvsH.toString());
  const ctx=cvs.getContext("2d");
  let r, g, b;
  let i;
  let j = 0;
  while (j < cvsH){
    i = 0;
    while (i < cvsW){
      r = Math.floor(Math.random() * Math.floor(256));
      g = Math.floor(Math.random() * Math.floor(256));
      b = Math.floor(Math.random() * Math.floor(256));
      ctx.fillStyle = ["rgba(", r.toString(), ",", g.toString(), ",",
          b.toString(), ",0.3)"].join('');
      ctx.fillRect(i, j, 20, 20);
      i += 24;
    }
    j += 24;
  }
  cvs.id = GRPH_SC;
  bdyObj.appendChild(cvs);
}

function deleteGrphSc(){
  const grphObj = document.getElementById(GRPH_SC);
  if (grphObj){
    const bdyObj = grphObj.parentNode;
    bdyObj.removeChild(grphObj);
  }
}

function figPrn(){
  window.print();
}

function listCpy(cpyElement){
  const parentElement = cpyElement.parentElement;
  cpyElement.className = 'cpying';
  if (parentElement) {
    const listId = parentElement.id.split('pyF')[1];
    const listElement = document.getElementById(listId);
    if (listElement){
      const regexNbsp = /[\u00a0]/g;
      const regexNoChar = /(\r?\n){2,}/g;
      let text = listElement.innerText;
      text = text.replace(regexNbsp, ' ');
      text = text.replace(regexNoChar, '$1');
      navigator.clipboard.writeText(text).then(
      function(){
        setTimeout(function(){listCpyEnd(cpyElement);}, 1000);
      }, function(){
        listCpyEnd(cpyElement);
      });
    }
  }
}

function listCpyEnd(cpyElement){
  cpyElement.className = 'cpy';
}

function listSwitch(listId){
  const cpyId = ['cpyF', listId].join('');
  let listElement = document.getElementById(listId);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(cpyId);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    } else {
      listElement.className = INACTLIST;
      listElement = document.getElementById(cpyId);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function listSwitchP(listId){
  const prnId = ['prn', listId].join('');
  let listElement = document.getElementById(listId);
  if (listElement){
    if (ACTLIST != listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(prnId);
      if (listElement){
        if (ACTPRN != listElement.className){
          listElement.className = ACTPRN;
        }
      }
    } else {
      listElement.className = INACTLIST;
      listElement = document.getElementById(prnId);
      if (listElement){
        if (INACTPRN != listElement.className){
          listElement.className = INACTPRN;
        }
      }
    }
  }
}

function listSwitchE(listId){
  const cpyId = ['cpyF', listId].join('');
  let listElement = document.getElementById(listId);
  if (listElement){
    if (INACTLIST == listElement.className){
      listElement.className = ACTLIST;
      listElement = document.getElementById(cpyId);
      if (listElement){
        if (ACTCPY != listElement.className){
          listElement.className = ACTCPY;
        }
      }
    } else if (ACTLIST == listElement.className){
      listElement.className = V_ACTLIST;
    } else if (V_ACTLIST == listElement.className){
      listElement.className = H_ACTLIST;
    } else {
      listElement.className = INACTLIST;
      listElement = document.getElementById(cpyId);
      if (listElement){
        if (INACTCPY != listElement.className){
          listElement.className = INACTCPY;
        }
      }
    }
  }
}

function wdListSwitch(listId, linkLines){
  let lineElement;
  let res1, res2;
  let newList;
  let strHtml;
  let elements;
  const wdId = listId.split('Z')[1];
  let listElement = document.getElementById(listId);
  if (listElement){
    if (ACTLIST == listElement.className){
      listElement.className = INACTLIST;
    } else {
      if ('' == listElement.innerHTML) {
        const spanElement = document.getElementById(wdId);
        const searchWd = spanElement.textContent;
        newList = [
            '<div><span class="wdcpy"',
            ` onclick="wdCpy(this, '`, searchWd, `')">copy `, searchWd,
            '</span></div>'].join('');
        let searchUri = [
            'https://google.com/search?ie=utf-8&q="',
            searchWd, '"'].join('');
        let searchUrl = encodeURI(searchUri);
        newList = [
            newList, '<a href="', searchUrl,
            '" target="_blank"><span class="search">→Search</span> "',
            '<span class="search-wd">', searchWd, '</span>"',
            ' by Google Web Search</a><br>'].join('');
        const searchEwd = [
            'translate ', searchWd, ' to english'].join('');
        searchUri = [
            'https://google.com/search?ie=utf-8&q="',
            searchEwd, '"'].join('');
        searchUrl = encodeURI(searchUri);
        newList = [
            newList, '<a href="', searchUrl,
            '" target="_blank"><span class="search">→Translate</span> "',
            '<span class="search-wd">', searchWd, '</span>"',
            ' by Google Web Search</a><br>'].join('');
        res1 = linkLines.split(',');
        for(let i1 in res1){
          res2 = res1[i1].split('/');
          let tmpList = [
              '<span class="llink" onclick="line(',
              "'", res2[0], "')", '">'].join('');
          if ('c' == res2[0].charAt(0)) {
            tmpList += '■CL-';
          } else {
            tmpList += '■明細';
          }
          tmpList += res2[0].slice(1) + "</span>";
          if ('0' != res2[1]) {
            tmpList = [
                tmpList, '(<span class="clink" onclick="cl(', "'cl", res2[1],
                "')", '">請求項', res2[1], "</span>)"].join('');
          }
          if ('0' != res2[2]) {
            tmpList = [
                tmpList, '(<span class="plink" onclick="spc(', "'pa",
                res2[2], "')", '">段落', res2[2], "</span>)"].join('');
          }
          lineElement = document.getElementById(res2[0]);
          strHtml = lineElement.innerHTML;
          newList = [
              newList, tmpList, "：", strHtml].join('');
        }
        listElement.textContent = '';
        listElement.insertAdjacentHTML("beforeend", newList);
        elements = listElement.getElementsByClassName(wdId);
        for(let i = 0; i < elements.length; i++) {
          elements[i].style.color = "#c09";
        }
      }
      listElement.className = ACTLIST;
    }
  }
}

function wdListListSwitch(listId){
  const regexNbsp = /[\u00a0]/g;
  let enWords = [];
  let strHtml = '';
  const enWordFieldId = ['ef', listId].join('');
  const wdId = listId.slice(1);
  const enWdId = ['E', wdId].join('');
  const wdElement = document.getElementById(wdId);
  if (wdElement) {
    const listElement = document.getElementById(listId);
    if (listElement){
      if (ACTLIST == listElement.className) {
        listElement.className = INACTLIST;
      } else {
        const wd = wdElement.textContent;
        const enWdElement = document.getElementById(enWdId);
        if (enWdElement) {
          let strEnWords = enWdElement.textContent;
          if (strEnWords) {
            if ('▲' == strEnWords[0]) {
              strEnWords = strEnWords.slice(1);
            }
            if (strEnWords) {
              enWords = strEnWords.split('/');
            }
          }
        }
        let searchUri = [
            'https://google.com/search?ie=utf-8&q="', wd, '"'].join('');
        let searchUrl = encodeURI(searchUri);
        newList = [
            '<a href="', searchUrl,
            '" target="_blank"><span class="search">→Search</span> "',
            '<span class="search-wd">', wd, '</span>"',
            ' by Google Web Search</a><br>'].join('');
        const searchEwd = [
            'translate ', wd, ' to english'].join('');
        searchUri = [
            'https://google.com/search?ie=utf-8&q="',
            searchEwd, '"'].join('');
        searchUrl = encodeURI(searchUri);
        newList = [
            newList, '<a href="', searchUrl,
            '" target="_blank"><span class="search">→Translate</span> "',
            '<span class="search-wd">', wd, '</span>"',
            ' by Google Web Search</a><br>'].join('');
        let lineId
        let efLineElement
        let efLine
        let regexEnWord
        if (wd in ARRAY_EF){
          const ef_line_refs = ARRAY_EF[wd].split('@@');
          const ef_lines = ef_line_refs[0].split('/');
          const ef_refs = ef_line_refs[1].split('@');
          for (let line_no=0; line_no < ef_lines.length; line_no++){
            lineId = ['en', ef_lines[line_no]].join('');
            efLineElement = document.getElementById(lineId);
            efLine = efLineElement.textContent.replace(regexNbsp, ' ');
            if (enWords.length) {
              for(let n = 0; n < enWords.length; n++) {
                for (let r = 0; r < ef_refs.length; r++){
                  regexEnWord = new RegExp(
                      ['(', enWords[n], ') (', ef_refs[r], ')'].join(''),
                      'gi');
                  efLine = efLine.replace(
                      regexEnWord, '<span class="exwd">$1</span> $2')
                }
              }
            }
            newList = [
                newList, '<span class="llink" onclick="line(',
                "'", lineId, "')", '">■関連表現</span>：<span>',
                efLine, '</span><br>'].join('');
          }
        }
        if (enWords.length) {
          let optionData = '';
          for(let i = 0; i < enWords.length; i++) {
            optionData = [
                optionData, '<option value="',
                enWords[i], '"></option>'].join('');
          }
          strHtml = [
              '<input class="enWordField" id="', enWordFieldId,
              '" type="text" value="" placeholder="', wd, 'の英語表現"',
              ' list="combo', enWordFieldId,
              `" onkeypress="entkyInput('`, enWordFieldId, `')">`,
              '<span class="enWordFieldBtn"',
              ` onclick="getEnWord('`, enWordFieldId, `')">`,
              '決定</span>',
              '<datalist id="combo', enWordFieldId, '">',
              optionData, '</datalist>',
              '<div><span class="wdcpy"',
              ` onclick="wdCpy(this, '`, wd, `')">copy `, wd,
              '</span></div>',
              '<div>', newList, '</div>'].join('');
        } else {
          strHtml = [
              '<input class="enWordField" id="', enWordFieldId,
              '" type="text" value="" placeholder="', wd, 'の英語表現"',
              ` onkeypress="entkyInput('`, enWordFieldId, `')">`,
              '<span class="enWordFieldBtn"',
              ` onclick="getEnWord('`, enWordFieldId, `')">`,
              '決定</span>',
              '<div><span class="wdcpy"',
              ` onclick="wdCpy(this, '`, wd, `')">copy `, wd,
              '</span></div>',
              '<div>', newList, '</div>'].join('');
        }
        listElement.textContent = '';
        listElement.insertAdjacentHTML("beforeend", strHtml);
        listElement.className = ACTLIST;
        const enWordFieldElement = document.getElementById(enWordFieldId);
        if (enWordFieldElement){
          enWordFieldElement.focus();
        }
      }
    }
  }
}

function entkyInput(inputFieldId){
  if (13 == event.keyCode){
    getEnWord(inputFieldId);
  }
}

function getEnWord(inputFieldId){
  const listId = inputFieldId.slice(2);
  const enWdId = ['E', listId.slice(1)].join('');
  const enWdClassName = ['e', listId.slice(1)].join('');
  const inputFieldElement = document.getElementById(inputFieldId);
  if (inputFieldElement){
    const listElement = document.getElementById(listId);
    if (listElement){
      listElement.className = INACTLIST;
    }
    const ewd = inputFieldElement.value;
    if (ewd){
      const enWdElement = document.getElementById(enWdId);
      if (enWdElement){
        enWdElement.textContent = ewd;
        if (false == enWdElement.classList.contains("p")){
          enWdElement.classList.add("p");
        }
      }
      let emixlistElement = document.getElementById(CL_JELIST);
      let elements = emixlistElement.getElementsByClassName(enWdClassName);
      for(let i = 0; i < elements.length; i++) {
        elements[i].textContent = ewd;
        if (elements[i].classList.contains("b")){
          elements[i].classList.remove("b");
        }
        if (elements[i].classList.contains("y")){
          elements[i].classList.remove("y");
        }
        if (false == elements[i].classList.contains("p")){
          elements[i].classList.add("p");
        }
      }
      emixlistElement = document.getElementById(SPC_JELIST);
      elements = emixlistElement.getElementsByClassName(enWdClassName);
      for(let i = 0; i < elements.length; i++) {
        elements[i].textContent = ewd;
        if (elements[i].classList.contains("b")){
          elements[i].classList.remove("b");
        }
        if (elements[i].classList.contains("y")){
          elements[i].classList.remove("y");
        }
        if (false == elements[i].classList.contains("p")){
          elements[i].classList.add("p");
        }
      }
    }
  }
}

function wdCpy(wdCpyElement,wd){
  wdCpyElement.className = 'wdcpying';
  const regexNbsp = /[\u00a0]/g;
  let text = wd.replace(regexNbsp, ' ');
  navigator.clipboard.writeText(text).then(
  function(){
    setTimeout(function(){wdCpyEnd(wdCpyElement);}, 500);
  }, function(){
    wdCpyEnd(wdCpyElement);
  });
}

function wdCpyEnd(wdCpyElement){
  wdCpyElement.className = 'wdcpy';
}

function transformCl(){
  let strClNumber;
  let clStr;
  const listElement = document.getElementById(SPC_JPLIST);
  const elements = listElement.getElementsByClassName(CL_ABBR);
  for (let i = 0; i < elements.length; i++) {
    strClNumber = elements[i].title;
    if ('■' == elements[i].textContent[0]) {
      if (!(strClNumber in a_array_cl_abbr)) {
        a_array_cl_abbr[strClNumber] = elements[i].textContent;
      }
      if (strClNumber in ARRAY_CL){
        clStr = ARRAY_CL[strClNumber];
      } else {
        clStr = [
            '（■Warning:', strClNumber, 'が存在しません。）'].join('');
      }
      elements[i].textContent = '';
      elements[i].insertAdjacentHTML("beforeend", clStr);
    } else {
      clStr = a_array_cl_abbr[strClNumber];
      elements[i].textContent = '';
      elements[i].insertAdjacentHTML("beforeend", clStr);
    }
  }
}
