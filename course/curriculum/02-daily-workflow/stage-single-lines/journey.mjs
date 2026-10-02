// Course journey: one hunk that holds two ideas; pick the lines of one of them, stage only those, commit.
// Starts at the `mixed-lines` checkpoint of course/demo-repo; markers are what beats.yml refers to.
export default {
  name: 'stage-single-lines',
  wip: false,
  quietTooltips: true,
  park: { x: 900, y: 560 },

  async prepare() {},

  async run(ui) {
    await ui.mark('start');
    await ui.sleep(2600); // the graph, with the Working changes row at the top

    await ui.mark('wip-before');
    await ui.click('button', /^Working changes: /, { first: true, after: 1200 });
    await ui.mark('wip-after');
    await ui.sleep(1300);

    await ui.mark('file-before');
    await ui.click('option', /^Modified src\/search\/index.ts/, { after: 1500 });
    const hunk = await ui.find('region', /^Hunk 1 of 1/);
    await ui.mark('hunk-shown');
    await ui.mark('hunk', hunk);
    await ui.sleep(4200); // the viewer reads the one hunk with its two ideas

    await ui.mark('pick-before');
    const first = await ui.find('checkbox', /^Pick line \+\d+: \/\*\* How many distinct words/);
    const last = await ui.find('checkbox', /^Pick line \+\d+: *$/);
    await ui.hoverSelector(first, { duration: 900 });
    await ui.sleep(1800);
    await ui.clickSelector(first, { after: 1800 });
    await ui.mark('first-picked');
    await ui.shiftClickSelector(last, { after: 1500 });
    await ui.mark('picked');
    const lines = await ui.rectOf([first, last]); // the picked lines, as wide as the hunk
    const wide = await ui.box(hunk);
    await ui.mark('range', { x: wide.x + 6, y: lines.y - 2, w: wide.w - 12, h: lines.h + 4 });
    await ui.sleep(1800);

    await ui.mark('stage-before');
    const stage = await ui.find('button', 'Stage Lines');
    await ui.mark('stage-button', stage);
    await ui.hoverSelector(stage, { duration: 800 });
    await ui.sleep(1400);
    await ui.clickSelector(stage, { after: 1900 });
    await ui.mark('stage-after');

    const rows = await ui.queryAll({ role: 'option', name: /^Modified src\/search\/index.ts/ }); // [0] unstaged, [1] staged
    const unstagedList = rows[0].selector;
    const stagedList = rows[1].selector;
    await ui.mark('unstaged-row', unstagedList);
    await ui.mark('staged-row', stagedList);
    await ui.mark('lists-begin');
    await ui.hoverSelector(unstagedList, { at: [0.3, 0.5], duration: 700 });
    await ui.sleep(3000);
    await ui.mark('lists-mid');
    await ui.clickSelector(stagedList, { after: 1500 }); // the staged copy: only the new method
    const stagedHunk = await ui.find('region', /^Hunk 1 of 1/);
    await ui.mark('staged-view', stagedHunk);
    await ui.sleep(3600);
    await ui.mark('staged-view-end');

    const summary = await ui.find('textbox', /^Summary/);
    await ui.mark('summary', summary);
    await ui.mark('msg-before');
    await ui.clickSelector(summary, { after: 400 });
    await ui.type('feat(search): add size()', { delay: 52 });
    await ui.mark('typed');
    await ui.sleep(500);
    await ui.mark('commit-before');
    const commit = await ui.find('button', /^Commit Changes to 1 File/);
    await ui.mark('commit-button', commit);
    await ui.clickSelector(commit, { after: 1800 });
    await ui.mark('commit-after');
    await ui.sleep(600);

    await ui.click('option', /^Modified src\/search\/index.ts/, { after: 1500 }); // what is left: the tags change
    await ui.mark('rest-begin');
    await ui.hoverSelector('body', { at: [0.5, 0.95], duration: 700 });
    await ui.sleep(3000);
    await ui.mark('rest-end');
    await ui.mark('end');
    await ui.sleep(500);
  },
};
