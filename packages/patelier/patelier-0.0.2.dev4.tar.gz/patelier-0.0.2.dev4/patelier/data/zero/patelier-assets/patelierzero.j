const P_HX = 'patelier.html';
const BRIGHT = 'bright';
const DIM = 'dim';
const DARK = 'dark';
const SCT_RT = 'sctRt';
const W8_SC = 'w8Sc';
const W8_SC_LT = 'w8ScLt';
const BK_SC = 'bkSc';
const TIME = 'time';
const GRPH_SCRT = "grphScRt";
const STATUS = 'status';
const INPUTFILE = 'inputFile';
const LNKTGT = 'lnkTgt';
const VER = 'ver';

function bdyActivate(){
  let bdyObj;
  dimToBright(SCT_RT);
  const wObj = document.getElementById(W8_SC);
  if (wObj){
    bdyObj = wObj.parentNode;
    bdyObj.removeChild(wObj);
  }
  const wObjLt = document.getElementById(W8_SC_LT);
  if (wObjLt){
    bdyObj = wObjLt.parentNode;
    bdyObj.removeChild(wObjLt);
  }
  const bsObj = document.getElementById(BK_SC);
  if (bsObj){
    bdyObj = bsObj.parentNode;
    bdyObj.removeChild(bsObj);
  }
  const img = document.getElementById(TIME);
  if (img){
    bdyObj = img.parentNode;
    bdyObj.removeChild(img);
  }
}

function bdyInactivate(){
  const bdyObj = document.getElementsByTagName('body').item(0); 
  brightToDim(SCT_RT);
  const rc = bdyObj.getBoundingClientRect();
  const cvsW = rc.width;
  const cvsH = rc.height;
  const cvs = document.createElement('canvas'); 
  cvs.setAttribute("width", cvsW.toString());
  cvs.setAttribute("height", cvsH.toString());
  const ctx=cvs.getContext("2d");
  let i;
  let j = 0;
  while (j < cvsH){
    i = 0;
    while (i < cvsW){
      if ((i+j) % 48){
        ctx.fillStyle = "rgba(192, 192, 192, 0.1)";
        ctx.fillRect(i, j, 20, 20);
      }
      i += 24;
    }
    j += 24;
  }
  cvs.id = W8_SC;
  bdyObj.appendChild(cvs);
  const cvsc = document.createElement('canvas'); 
  cvsc.setAttribute("width", cvsW.toString());
  cvsc.setAttribute("height", cvsH.toString());
  const ctxc=cvsc.getContext("2d");
  let r, g, b;
  j = 0;
  while (j < cvsH){
    i = 0;
    while (i < cvsW){
      r = Math.floor(Math.random() * Math.floor(256));
      g = Math.floor(Math.random() * Math.floor(256));
      b = Math.floor(Math.random() * Math.floor(256));
      ctxc.fillStyle = ["rgba(", r.toString(), ",", g.toString(), ",",
          b.toString(), ",0.2)"].join('');
      ctxc.fillRect(i, j, 20, 20);
      i += 24;
    }
    j += 24;
  }
  cvsc.id = BK_SC;
  bdyObj.appendChild(cvsc);
  const img = document.createElement('div');
  img.id = TIME;
  bdyObj.appendChild(img);
  const iRect = bdyObj.getBoundingClientRect();
  let scale;
  if (iRect.width > iRect.height){
    scale = iRect.width / iRect.height;
  } else {
    scale = iRect.height / iRect.width;
  }
  strScale = scale.toString();
  const css = document.createElement('style');
  css.media = 'screen';
  css.type = 'text/css';
  turn = [
      '@keyframes turn {', [
      '0% {transform: scale(', strScale, ') rotate(0turn);}',
      '100% {transform: scale(', strScale, ') rotate(1turn);}'
      ].join(' '), '}'].join('');
  rule = document.createTextNode(turn);
  css.appendChild(rule);
  document.getElementsByTagName('head')[0].appendChild(css);
}

function bdyInactivateLt(){
  const wObjLt = document.createElement('div'); 
  wObjLt.id = W8_SC_LT; 
  const bdyObj = document.getElementsByTagName('body').item(0); 
  bdyObj.appendChild(wObjLt);
}

function initialize(){
  eel.py_showver();
  srcListProc();
}

function srcListProc(){
  eel.py_srclist();
  document.getElementById(STATUS).textContent =
      '■原文(請求項を含むtext/document)を指定してください。';
}

function remove_dir(dirname){
  bdyInactivateLt();
  eel.py_rmdir(dirname);
}

function readClipboard(){
  bdyInactivate();
  eel.py_clip();
}

function inputFileProc(){
  eel.py_fileanalyze();
}

function brightToDim(sctId){
  const sctElement = document.getElementById(sctId);
  if (sctElement){
    if (BRIGHT == sctElement.className){
      sctElement.className = DIM;
    }
  }
}

function dimToBright(sctId){
  const sctElement = document.getElementById(sctId);
  if (sctElement){
    if (DIM == sctElement.className){
      sctElement.className = BRIGHT;
    }
  }
}

function sctColorChgz(sctId){
  const sctElement = document.getElementById(sctId);
  if (sctElement){
    if (BRIGHT == sctElement.className){
      sctElement.className = DARK;
    } else {
      sctElement.className = BRIGHT;
    }
  }
}

function chgColorz(){
  showGrphSc();
  setTimeout(deleteGrphSc, 2000);
  sctColorChgz(SCT_RT);
}

function showGrphSc(){
  const bdyObj = document.getElementsByTagName('body').item(0); 
  const rc = bdyObj.getBoundingClientRect();
  const cvsW = rc.width;
  const cvsH = rc.height;
  const cvs = document.createElement('canvas'); 
  cvs.setAttribute("width", cvsW.toString());
  cvs.setAttribute("height", cvsH.toString());
  const ctx=cvs.getContext("2d");
  let i;
  let j = 0;
  while (j < cvsH){
    i = 0;
    while (i < cvsW){
      if ((i+j) % 48){
        ctx.fillStyle = "rgba(64,64,64,0.1)";
      } else {
        ctx.fillStyle = "rgba(192,192,192,0.1)";
      }
      ctx.fillRect(i, j, 20, 20);
      i += 24;
    }
    j += 24;
  }
  cvs.id = GRPH_SCRT;
  bdyObj.appendChild(cvs);
}

function deleteGrphSc(){
  const grphObj = document.getElementById(GRPH_SCRT);
  if (grphObj){
    const bdyObj = grphObj.parentNode;
    bdyObj.removeChild(grphObj);
  }
}

eel.expose(jsFReadComp);
function jsFReadComp() {
  bdyInactivate();
}

eel.expose(jsFReadErr);
function jsFReadErr() {
  jsDispStat('■原文ファイル読込に失敗しました。');
}

eel.expose(jsDispStat);
function jsDispStat(status) {
  const element = document.getElementById(STATUS);
  if (element){
    element.textContent = status;
  }
}

eel.expose(jsDispVer);
function jsDispVer(ver) {
  const element = document.getElementById(VER);
  if (element){
    element.textContent = ver;
  }
}

eel.expose(jsDispSrcList);
function jsDispSrcList(values) {
  let str_linklist = '<ul>';
  for (let i = 0; i < values.length; i++){
    let strdir = values[i];
    let str_eachlink = [
        '<li><button id="', strdir,
        '" onclick="remove_dir(this.id)">原文Listから削除→</button>&nbsp;',
        '<a href="./', strdir, '/', P_HX, '" target="_blank">', strdir,
        '</a></li>'].join('');
    str_linklist = [
        str_linklist, str_eachlink].join('');
  }
  str_linklist += '</ul>';
  document.getElementById(LNKTGT).innerHTML = str_linklist
  bdyActivate();
}
