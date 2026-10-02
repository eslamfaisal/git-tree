// Course journey: create a repository from the New Tab page with the Init dialog.
// Starts on the New Tab page (`openRepo: false`, no repository). The folder is a new one in a temp location:
// the app's native folder picker cannot be driven under WebDriver, so the path is typed into Location.
import { mkdirSync, rmSync } from 'node:fs';

const PROJECTS = '/tmp/projects';
const FOLDER = `${PROJECTS}/recipe-box`;

export default {
  name: 'init-a-repository',
  openRepo: false,
  wip: false,
  quietTooltips: true,
  park: { x: 1000, y: 640 },

  async prepare() {
    // The parent exists, the folder does not: GitTree creates it. (GitTree refuses a folder that is not empty.)
    rmSync(FOLDER, { recursive: true, force: true });
    mkdirSync(PROJECTS, { recursive: true });
  },

  async run(ui, browser) {
    await ui.mark('start');
    await ui.sleep(1000); // the New Tab page: Open, Clone, Init

    const initCard = await ui.find('button', /^Init/);
    await ui.mark('init-card', initCard);
    await ui.mark('card-before');
    await ui.hoverSelector(initCard, { duration: 900 });
    await ui.sleep(1000);
    await ui.clickSelector(initCard, { after: 900 });
    const dialog = await ui.dialog('Initialize a repository');
    await ui.mark('dialog-box', dialog);
    await ui.mark('dialog-open');
    await ui.sleep(1500); // "Nothing is written until you choose Initialize."

    // Location
    const location = await ui.find('textbox', 'Location');
    await ui.mark('location-box', location);
    await ui.mark('location-before');
    await ui.clickSelector(location, { after: 400 });
    await ui.type(FOLDER, { delay: 60 });
    await ui.mark('location-typed');
    await ui.sleep(1300);

    // Initial branch, then the bare-repository checkbox (left unchecked)
    const branch = await ui.find('textbox', 'Initial branch');
    await ui.mark('branch-box', branch);
    await ui.mark('branch-before');
    await ui.hoverSelector(branch, { duration: 800 });
    await ui.sleep(2200);
    await browser.execute(`
      const label = [...document.querySelectorAll('label')].find((l) => l.textContent.startsWith('Bare repository'));
      label.parentElement.setAttribute('data-course', 'bare');`);
    await ui.mark('bare-box', '[data-course="bare"]');
    await ui.mark('bare-before');
    await ui.hoverSelector('[data-course="bare"]', { at: [0.3, 0.5], duration: 800 });
    await ui.sleep(2400);

    // Starting files: a .gitignore template and a licence
    const gitignore = await ui.find('combobox', '.gitignore template');
    await ui.mark('gitignore-box', gitignore);
    await ui.mark('templates-before');
    await ui.clickSelector(gitignore, { after: 600 });
    await ui.sleep(600);
    await ui.click('option', 'Node.js', { after: 800 });
    await ui.mark('gitignore-chosen');
    const licence = await ui.find('combobox', 'Licence');
    await ui.mark('licence-box', licence);
    await ui.clickSelector(licence, { after: 600 });
    await ui.sleep(500);
    await ui.click('option', 'MIT License', { after: 800 });
    await ui.mark('licence-chosen');
    const holder = await ui.find('textbox', 'Copyright holder');
    await ui.mark('holder-box', holder);
    await ui.clickSelector(holder, { after: 300 });
    await ui.type('Maya Chen', { delay: 60 });
    await ui.mark('holder-typed');
    await ui.sleep(700);

    // Open after creating, then Initialize
    const openAfter = await ui.find('checkbox', 'Open after creating');
    await ui.mark('open-after-box', openAfter);
    await ui.mark('open-after-before');
    await ui.hoverSelector(openAfter, { duration: 800 });
    await ui.sleep(1000);
    const submit = await ui.find('button', 'Initialize');
    await ui.mark('submit-box', submit);
    await ui.mark('submit-before');
    await ui.clickSelector(submit, { after: 1800 });
    await ui.mark('created'); // the new repository is open: no commits yet, two files waiting
    await ui.sleep(1000);

    const wip = await ui.find('button', /^Working changes: /, { first: true });
    await ui.mark('wip-row', wip);
    await ui.mark('wip-before');
    await ui.clickSelector(wip, { after: 1300 });
    await ui.mark('wip-after');
    await ui.sleep(1500);
    await ui.mark('end');
    await ui.sleep(500);
  },
};
