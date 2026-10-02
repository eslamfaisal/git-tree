// Course journey: stage one hunk of a file, commit it, and show the other hunk is still waiting.
// Starts at the `two-hunks` checkpoint of course/demo-repo; markers are what beats.yml refers to.
export default {
  name: 'stage-hunk',
  wip: false,
  quietTooltips: true,
  park: { x: 900, y: 560 },

  async prepare() {},

  async run(ui) {
    await ui.mark('start');
    await ui.sleep(3600); // the graph, with the Working changes row at the top

    await ui.mark('wip-before');
    await ui.click('button', /^Working changes: /, { first: true, after: 1200 });
    await ui.mark('wip-after');
    await ui.sleep(1300);

    await ui.mark('file-before');
    await ui.click('option', /^Modified src\/search\/index.ts/, { after: 1500 });
    const hunk1 = await ui.find('region', /^Hunk 1 of 2/);
    const hunk2 = await ui.find('region', /^Hunk 2 of 2/);
    await ui.mark('hunks-shown');
    await ui.mark('hunk1', hunk1);
    await ui.mark('hunk2', hunk2);
    await ui.sleep(2600); // the viewer reads the two hunks

    await ui.mark('stage-before');
    const stage = await ui.find('button', /^Stage Hunk — Hunk 1 of 2/);
    await ui.mark('stage-button', stage);
    await ui.hoverSelector(stage, { duration: 900 });
    await ui.sleep(2200); // the pointer rests on the button while it is explained
    await ui.clickSelector(stage, { after: 1900 });
    await ui.mark('stage-after');

    const rows = await ui.queryAll({ role: 'option', name: /^Modified src\/search\/index.ts/ }); // [0] unstaged, [1] staged
    const unstagedList = rows[0].selector;
    const stagedList = rows[1].selector;
    await ui.mark('unstaged-row', unstagedList);
    await ui.mark('staged-row', stagedList);
    await ui.mark('lists-begin');
    await ui.hoverSelector(unstagedList, { at: [0.3, 0.5], duration: 700 });
    await ui.sleep(4200);
    await ui.mark('lists-mid');
    await ui.hoverSelector(stagedList, { at: [0.3, 0.5], duration: 700 });
    await ui.sleep(3600);
    await ui.mark('lists-end');

    await ui.mark('staged-view-before');
    const options = await ui.queryAll({ role: 'option', name: /^Modified src\/search\/index.ts/ });
    await ui.clickSelector(options[1].selector, { after: 1500 }); // the staged copy of the file
    const stagedHunk = await ui.find('region', /^Hunk 1 of 1/);
    await ui.mark('staged-view', stagedHunk);
    await ui.sleep(3800);
    await ui.mark('staged-view-end');

    const summary = await ui.find('textbox', /^Summary/);
    await ui.mark('summary', summary);
    await ui.mark('msg-before');
    await ui.clickSelector(summary, { after: 400 });
    await ui.type('docs(search): describe the inverted index', { delay: 52 });
    await ui.mark('typed');
    await ui.sleep(700);
    await ui.mark('commit-before');
    await ui.click('button', /^Commit Changes to 1 File/, { after: 1800 });
    await ui.mark('commit-after');
    await ui.sleep(900);

    await ui.click('option', /^Modified src\/search\/index.ts/, { after: 1400 }); // what is left: the unstaged copy
    await ui.mark('rest-begin');
    await ui.hoverSelector('body', { at: [0.5, 0.6], duration: 700 });
    await ui.sleep(4400); // the other hunk is still unstaged
    await ui.mark('rest-end');

    await ui.mark('close-before');
    await ui.click('button', 'Close Diff', { after: 1500 });
    await ui.mark('graph-after');
    await ui.sleep(1200);
    const row = await ui.find('row', /^commit [0-9a-f]+, main, checked-out branch, docs\(search\): describe the inverted index/);
    await ui.mark('new-commit-row', row);
    await ui.mark('select-before');
    await ui.clickSelector(row, { after: 1600 });
    await ui.hoverSelector('body', { at: [0.62, 0.9], duration: 600 });
    await ui.mark('commit-selected');
    await ui.sleep(1800);
    await ui.mark('commit-file-before');
    await ui.click('treeitem', /^src\/search\/index\.ts, modified/, { after: 1700 });
    await ui.hoverSelector('body', { at: [0.45, 0.97], duration: 500 }); // no tooltip over the picture
    await ui.mark('commit-diff');
    await ui.sleep(2800);
    await ui.mark('end');
    await ui.sleep(500);
  },
};
