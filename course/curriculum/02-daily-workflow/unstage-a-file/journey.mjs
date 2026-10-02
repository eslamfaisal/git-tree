// Course journey: unstage one of two staged files, check nothing was lost, then unstage the other with the U key.
// Starts at the `two-files-modified` checkpoint of course/demo-repo, with both files already staged (prepare); markers are what beats.yml refers to.
export default {
  name: 'unstage-a-file',
  wip: false,
  quietTooltips: true,
  park: { x: 900, y: 560 },

  async prepare(ui) {
    await ui.click('button', /^Working changes: /, { first: true, after: 900 });
    await ui.click('button', 'Stage All Changes', { after: 1200 }); // the lesson starts with two staged files
    await ui.find('option', /^Modified src\/tags\.ts/);
  },

  async run(ui) {
    await ui.mark('start');
    const staged = await ui.find('listbox', /^Staged Files, 2 files/);
    await ui.mark('staged-box', staged);
    await ui.mark('open-staged');
    await ui.sleep(12000); // the two staged files stay on screen while they are named

    await ui.mark('unstage-before');
    const tags = await ui.find('option', /^Modified src\/tags\.ts/);
    await ui.mark('tags-row', tags);
    await ui.hoverSelector(tags, { at: [0.3, 0.5], duration: 900 });
    await ui.sleep(1400);
    const allRows = await ui.queryAll({ role: 'option', name: /^Modified / });
    const buttons = await ui.queryAll({ role: 'button', name: 'Unstage File' }); // one hidden button per row, in row order
    const unstage = buttons[allRows.findIndex((r) => /tags\.ts/.test(r.name))].selector;
    await ui.mark('unstage-button', unstage);
    await ui.hoverSelector(unstage, { duration: 700 });
    await ui.sleep(2400); // the pointer rests on the button while it is explained
    await ui.clickSelector(unstage, { after: 1800 });
    await ui.mark('unstage-after');

    const lists = await ui.queryAll({ role: 'option', name: /^Modified / });
    const names = lists.map((l) => l.name);
    await ui.mark('lists-begin');
    for (const l of lists) {
      if (/tags\.ts/.test(l.name)) await ui.mark('unstaged-row', l.selector);
      else await ui.mark('staged-row', l.selector);
    }
    await ui.sleep(3200);
    await ui.mark('lists-mid');
    await ui.sleep(3800);
    await ui.mark('lists-end');

    await ui.mark('still-before');
    const unstagedTags = await ui.find('option', /^Modified src\/tags\.ts/);
    await ui.clickSelector(unstagedTags, { after: 1600 });
    const hunk = await ui.find('region', /^Hunk 1 of 1/);
    await ui.mark('still-diff', hunk);
    await ui.sleep(4400); // the edit is still there
    await ui.mark('still-end');

    await ui.mark('key-before');
    const readme = await ui.find('option', /^Modified README\.md/);
    await ui.clickSelector(readme, { after: 1200 });
    await ui.sleep(1200);
    await ui.mark('key-press');
    await ui.keys(['u'], { after: 1800 });
    await ui.mark('key-after');
    await ui.hoverSelector('body', { at: [0.5, 0.9], duration: 600 });
    await ui.sleep(4800); // nothing is staged any more
    await ui.mark('end');
    await ui.sleep(500);
  },
};
