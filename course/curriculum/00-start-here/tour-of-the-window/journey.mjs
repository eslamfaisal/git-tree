// Course journey: the GitTree window tour. Starts at the `clean` checkpoint (lumen, no local changes).
// Toolbar, sidebar, graph, inspector, then the toggles (Ctrl+J, Ctrl+K, Alt+T) and Escape (Back).
export default {
  name: 'tour-of-the-window',
  wip: false,
  quietTooltips: true,
  park: { x: 1000, y: 640 },

  async prepare() {},

  async run(ui) {
    await ui.mark('start');
    await ui.sleep(900); // the whole window, nothing selected yet

    // Toolbar: left to right, then the three panel buttons (their tooltips name the shortcuts).
    const toolbar = await ui.find('toolbar', 'Application toolbar');
    await ui.mark('toolbar-box', toolbar);
    await ui.mark('toolbar-start');
    await ui.sleep(700);
    const undo = await ui.find('button', 'Undo');
    await ui.hoverSelector(undo, { duration: 700 });
    await ui.sleep(1100);
    const push = await ui.find('button', 'Push');
    await ui.hoverSelector(push, { duration: 800 });
    await ui.sleep(900);
    const terminal = await ui.find('button', 'Terminal', { first: true });
    await ui.hoverSelector(terminal, { duration: 800 });
    await ui.sleep(900);
    const sidebarBtn = await ui.find('button', 'Sidebar');
    const drawerBtn = await ui.find('button', 'Drawer');
    const inspectorBtn = await ui.find('button', 'Inspector');
    await ui.mark('panel-buttons', await ui.rectOf([sidebarBtn, drawerBtn, inspectorBtn]));
    await ui.mark('panel-buttons-start');
    await ui.hoverSelector(sidebarBtn, { duration: 900 });
    await ui.sleep(1050);
    await ui.hoverSelector(drawerBtn, { duration: 500 });
    await ui.sleep(1050);
    await ui.hoverSelector(inspectorBtn, { duration: 500 });
    await ui.sleep(1000);

    // Sidebar: sections, then the filter box.
    const sidebar = await ui.find('navigation', 'Repository navigation');
    await ui.mark('sidebar-box', sidebar);
    await ui.mark('sidebar-start');
    await ui.hoverSelector(sidebar, { at: [0.5, 0.45], duration: 900 });
    await ui.sleep(1900);
    const filter = await ui.find('textbox', 'Filter');
    await ui.mark('filter-box', filter);
    await ui.mark('filter-before');
    await ui.clickSelector(filter, { after: 400 });
    await ui.type('export', { delay: 80 });
    await ui.mark('filter-typed');
    await ui.sleep(1300);
    await ui.keys(['Control', 'a'], { after: 200 });
    await ui.keys(['Backspace'], { after: 500 });

    // Graph: one row per commit; select one.
    const graph = await ui.find('grid', 'Commit history');
    await ui.mark('graph-box', graph);
    await ui.mark('graph-start');
    await ui.hoverSelector(graph, { at: [0.6, 0.35], duration: 900 });
    await ui.sleep(1800);
    const row = await ui.find('row', /^commit [0-9a-f]+, docs: add a changelog/);
    await ui.mark('row-box', row);
    await ui.mark('row-before');
    await ui.clickSelector(row, { after: 1000 });
    await ui.mark('row-after');
    await ui.sleep(900);

    // Inspector: the selected commit's details.
    const inspector = await ui.find('complementary', 'Commit Details');
    await ui.mark('inspector-box', inspector);
    await ui.mark('inspector-start');
    await ui.hoverSelector(inspector, { at: [0.5, 0.25], duration: 900 });
    await ui.sleep(3000);

    // Toggles: Ctrl+J folds the sidebar to a strip, Ctrl+K hides the inspector; again brings each back.
    await ui.hoverSelector('body', { at: [0.62, 0.9], duration: 600 });
    await ui.mark('toggles-start');
    await ui.sleep(900);
    await ui.mark('keys-j');
    await ui.keys(['Control', 'j'], { after: 1000 });
    await ui.sleep(1500);
    await ui.mark('keys-j-back');
    await ui.keys(['Control', 'j'], { after: 900 });
    await ui.sleep(600);
    await ui.mark('keys-k');
    await ui.keys(['Control', 'k'], { after: 1000 });
    await ui.sleep(1500);
    await ui.mark('keys-k-back');
    await ui.keys(['Control', 'k'], { after: 900 });
    await ui.sleep(1300);

    // Drawer: Alt+T opens it (Terminal tab), the Activity Log tab lists git commands, Alt+T closes it.
    await ui.mark('drawer-start');
    await ui.sleep(700);
    await ui.mark('keys-t');
    await ui.keys(['Alt', 't'], { after: 1100 });
    const drawer = await ui.find('region', 'Bottom drawer');
    await ui.mark('drawer-box', drawer);
    await ui.sleep(1900);
    await ui.mark('activity-before');
    await ui.click('tab', 'Activity Log', { after: 1000 });
    await ui.mark('activity-after');
    await ui.sleep(1800);
    await ui.mark('keys-t-close');
    await ui.keys(['Alt', 't'], { after: 1000 });
    await ui.sleep(900);
    await ui.mark('drawer-end');

    // Back: Escape leaves a diff.
    await ui.mark('back-start');
    await ui.sleep(700);
    const file = await ui.find('treeitem', /^CHANGELOG\.md, /);
    await ui.mark('file-before');
    await ui.clickSelector(file, { after: 1200 });
    await ui.mark('diff-open');
    await ui.sleep(1700);
    await ui.mark('keys-esc');
    await ui.keys(['Escape'], { after: 1000 });
    await ui.mark('back-after');
    await ui.sleep(1300);
    await ui.mark('end');
    await ui.sleep(500);
  },
};
