// Course journey: stage the readme, write a summary and a description, commit with Ctrl+Enter, and show what is left.
// Starts at the `two-files-modified` checkpoint of course/demo-repo (two modified files, nothing staged); markers are what beats.yml refers to.
export default {
  name: 'make-a-commit',
  wip: false,
  quietTooltips: true,
  park: { x: 900, y: 560 },

  async prepare(ui) {
    await ui.click('button', /^Working changes: /, { first: true, after: 900 });
    await ui.find('option', /^Modified README\.md/);
  },

  async run(ui) {
    await ui.mark('start');
    await ui.sleep(1500);

    await ui.mark('stage-before');
    const readme = await ui.find('option', /^Modified README\.md/);
    await ui.hoverSelector(readme, { at: [0.3, 0.5], duration: 800 });
    await ui.sleep(1200);
    const buttons = await ui.queryAll({ role: 'button', name: 'Stage File' }); // one hidden button per row, in row order
    const rows = await ui.queryAll({ role: 'option', name: /^Modified / });
    const stage = buttons[rows.findIndex((r) => /README\.md/.test(r.name))].selector;
    await ui.hoverSelector(stage, { duration: 700 });
    await ui.sleep(1200);
    await ui.clickSelector(stage, { after: 1700 });
    await ui.mark('stage-after');
    const staged = await ui.find('listbox', /^Staged Files, 1 file/);
    await ui.mark('staged-box', staged);
    await ui.sleep(2400);

    await ui.sleep(3600); // the commit button now names one file
    const commitButton = await ui.find('button', /^Commit Changes to 1 File/);
    await ui.mark('commit-button', commitButton);

    const summary = await ui.find('textbox', /^Summary/);
    await ui.mark('summary', summary);
    await ui.mark('summary-before');
    await ui.clickSelector(summary, { after: 500 });
    await ui.type('docs(readme): add a Tags section', { delay: 55 });
    await ui.mark('typed');
    await ui.sleep(5000);
    await ui.mark('summary-end');

    const description = await ui.find('textbox', /^Description/);
    await ui.mark('description', description);
    await ui.mark('description-before');
    await ui.clickSelector(description, { after: 500 });
    await ui.type('Show how to tag a note.', { delay: 40 });
    await ui.sleep(2400);
    await ui.mark('description-end');

    await ui.mark('submit-before');
    await ui.hoverSelector(commitButton, { duration: 800 });
    await ui.sleep(6200); // the pointer rests on the button while it is explained
    await ui.mark('key-press');
    await ui.keys(['Control', 'Enter'], { after: 1800 });
    await ui.mark('submit-after');
    await ui.mark('rest-before'); // the toast: Committed <sha>
    const left = await ui.find('listbox', /^Unstaged Files, 1 file/);
    await ui.mark('left-box', left);
    await ui.hoverSelector('body', { at: [0.5, 0.97], duration: 600 });
    await ui.sleep(7800); // tags.ts is still waiting, unstaged
    await ui.mark('rest-end');

    await ui.mark('commit-view-before');
    const row = await ui.find('row', /^commit [0-9a-f]+, main, checked-out branch, docs\(readme\): add a Tags section/);
    await ui.mark('new-commit-row', row);
    await ui.clickSelector(row, { after: 1800 });
    await ui.hoverSelector('body', { at: [0.62, 0.95], duration: 600 });
    await ui.mark('commit-selected');
    await ui.sleep(5200);
    await ui.mark('end');
    await ui.sleep(500);
  },
};
