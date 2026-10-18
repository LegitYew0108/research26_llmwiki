import fs from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const root='C:/Users/legit/Documents/Univ/research26_llmwiki';
const skill='C:/Users/legit/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const p=Presentation.create({slideSize:{width:1280,height:720}});
const s=p.slides.add(); s.background.fill='#FFFFFF';
function text(t,x,y,w,h,size,color='#172D42',bold=false){const a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=t;a.text.style={typeface:'Yu Gothic',fontSize:size,color,bold};return a;}
text('SAILOR',60,35,1150,65,48,'#172D42',true);
text('短い動作系列をスキルとして検索・再利用',62,108,1150,55,32,'#172D42',true);
text('スキル表現の学習',65,200,390,44,28,'#172D42',true);
text('対象デモに近いスキル',460,200,440,44,28,'#008C95',true);
text('スキルを選ぶ方策',930,200,330,44,28,'#172D42',true);
const b=await fs.readFile(root+'/.build_sailor/figure1.png');
s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',alt:'SAILOR原論文Fig.1：スキル表現の学習、類似スキルの検索、潜在スキルを予測する方策の学習',fit:'contain',position:{left:65,top:260,width:1145,height:360}});
text('VAE＋時間差予測',65,620,390,42,27,'#172D42',true);
text('L2距離・上位n件',480,620,390,42,27,'#008C95',true);
text('デモ＋検索結果でBC',920,620,340,42,26,'#172D42',true);
text('Nasiriany et al., CoRL 2022 / PMLR 2023  Fig. 1 / §4',62,677,1150,25,16,'#66727C');
const notes=await fs.readFile(root+'/.build_sailor/notes.txt','utf8');
s.speakerNotes.text=notes;
await fs.writeFile(root+'/artifacts/sailor/speaker_notes.md',`---\ntitle: SAILOR 発表メモ\ntype: presentation-notes\ntags: [sailor, skill-learning, imitation-learning, presentation]\nsources:\n  - ../../raw/temp/nasiriany_2023_sailor.pdf\n  - ../../raw/papers/2304.08742v2.pdf\nupdated: 2026-10-19\n---\n\n# 発表原稿（約2〜3分）\n\n${notes}\n`);
await (await PresentationFile.exportPptx(p)).save(root+'/.build_sailor/candidate.pptx');
const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(root+'/artifacts/sailor/slide.png',new Uint8Array(await png.arrayBuffer()));
const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs').href);
console.log(await finalizePresentation({workspaceDir:root,candidatePath:root+'/.build_sailor/candidate.pptx',finalPath:root+'/artifacts/sailor/sailor.pptx',pythonExecutable:'C:/Users/legit/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],explicitTotalSlideCount:1,fontPolicy:{basis:'design',families:['Yu Gothic']},verifyArtifactToolImport:true,receiptPath:root+'/.build_sailor/validation.json'}));

