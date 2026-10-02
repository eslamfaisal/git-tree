// Course journey: stage one of two changed files, commit it, then stage the other with the S shortcut.
// Starts at the `two-files-modified` checkpoint of course/demo-repo; markers are what beats.yml refers to.
export default {
  name: 'stage-a-file',
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
    await ui.sleep(1500);

    // Two unrelated files wait under Unstaged Files.
    const readmeRow = await ui.find('option', /^Modified README\.md/);
    const tagsRow = await ui.find('option', /^Modified src\/tags\.ts/);
    await ui.mark('readme-row', readmeRow);
    await ui.mark('tags-row', tagsRow);
    await ui.mark('files-before');
    await ui.hoverSelector(tagsRow, { at: [0.3, 0.5], duration: 800 });
    await ui.sleep(2400);
    await ui.mark('files-end');

    await ui.mark('pick-before');
    await ui.clickSelector(tagsRow, { after: 1500 });
    await ui.mark('diff-shown');
    await ui.sleep(2600); // the viewer reads the diff of the one file

    // The Stage File button appears when the pointer is over the row.
    await ui.mark('stage-before');
    await ui.hoverSelector(tagsRow, { at: [0.3, 0.5], duration: 800 });
    await ui.sleep(900);
    const stage = `${tagsRow} button[aria-label="Stage File"]`; // this row's own button
    await ui.mark('stage-button', stage);
    await ui.hoverSelector(stage, { duration: 800 });
    await ui.sleep(2000);
    await ui.clickSelector(stage, { after: 1900 });
    await ui.mark('stage-after');

    const stagedRow = await ui.find('option', /^Modified src\/tags\.ts/);
    const stillUnstaged = await ui.find('option', /^Modified README\.md/);
    await ui.mark('staged-row', stagedRow);
    await ui.mark('unstaged-row', stillUnstaged);
    await ui.mark('lists-begin');
    await ui.hoverSelector(stagedRow, { at: [0.3, 0.5], duration: 700 });
    await ui.sleep(3200);
    await ui.mark('lists-mid');
    await ui.hoverSelector(stillUnstaged, { at: [0.3, 0.5], duration: 700 });
    await ui.sleep(3000);
    await ui.mark('lists-end');

    const summary = await ui.find('textbox', /^Summary/);
    await ui.mark('summary', summary);
    await ui.mark('msg-before');
    await ui.clickSelector(summary, { after: 400 });
    await ui.type('feat(tags): add sortTags', { delay: 52 });
    await ui.mark('typed');
    await ui.sleep(700);
    await ui.mark('commit-before');
    const commit = await ui.find('button', /^Commit Changes to 1 File/);
    await ui.mark('commit-button', commit);
    await ui.clickSelector(commit, { after: 1800 });
    await ui.mark('commit-after');
    await ui.sleep(1000);
    const left = await ui.find('option', /^Modified README\.md/);
    await ui.mark('left-row', left);
    await ui.hoverSelector(left, { at: [0.3, 0.5], duration: 700 });
    await ui.mark('left-begin');
    await ui.sleep(3600); // README is still waiting, untouched
    await ui.mark('left-end');

    // The keyboard way: select the row, press S.
    await ui.mark('key-before');
    await ui.clickSelector(left, { after: 1200 });
    await ui.mark('key-ready');
    await ui.sleep(1200);
    await ui.keys(['s'], { after: 1800 });
    await ui.mark('key-after');
    const moved = await ui.find('option', /^Modified README\.md/);
    await ui.mark('moved-row', moved);
    await ui.hoverSelector(moved, { at: [0.3, 0.5], duration: 700 });
    await ui.sleep(3200);
    await ui.mark('end');
    await ui.sleep(500);
  },
};
