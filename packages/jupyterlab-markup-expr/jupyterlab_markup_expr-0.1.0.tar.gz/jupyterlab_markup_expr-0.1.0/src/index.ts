import { expressionPlugin } from './plugin';
import { simpleMarkdownItPlugin } from '@agoose77/jupyterlab-markup';

const PACKAGE_NS = '@agoose77/jupyterlab-markup-expr';
/**
 * Captures expressions as data-attributes
 */
const plugin = simpleMarkdownItPlugin(PACKAGE_NS, {
  id: 'markdown-it-expr',
  title: 'Create spans with stored expressions from Markdown',
  description: 'Embed Markdown text in a data attribute in rendered spans',
  documentationUrls: {},
  plugin: async () => {
    return [expressionPlugin];
  }
});

export default plugin;
