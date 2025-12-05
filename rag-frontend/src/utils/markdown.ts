import { Marked, marked, type Token } from "marked";
import { bundledLanguages, bundledThemes, createHighlighter , type Highlighter } from "shiki";
import hljs from "highlight.js";
import DOMPurify from "dompurify";

type CodeToken = Token & {
  type: "code";
  text: string;
  lang?: string;
};

const highlightExtension = {
  extensions: [
    {
      name: "code",
      renderer(token: Token) {
        const codeToken = token as CodeToken;

        const highlighted =
          codeToken.lang && hljs.getLanguage(codeToken.lang)
            ? hljs.highlight(codeToken.text, { language: codeToken.lang }).value
            : hljs.highlightAuto(codeToken.text).value;

        return `<pre><code class="hljs">${highlighted}</code></pre>`;
      },
    },
  ],
};


marked.use(highlightExtension);

let highlighterPromise: Promise<Highlighter>;

function loadHighlighter(): Promise<Highlighter> {
  if (!highlighterPromise) {
    highlighterPromise = createHighlighter({
      themes: [bundledThemes["github-dark"]],
      langs: Object.values(bundledLanguages),
    });
  }
  return highlighterPromise;
}

const CODE_FENCE_REGEX = /```(\w+)?\n([\s\S]*?)```/g;

export async function renderMarkdown(md: string): Promise<string> {
  const highlighter = await loadHighlighter();

  const processed = await replaceAsync(
  md,
  CODE_FENCE_REGEX,
    async (
      _match: string,
      langRaw?: string,
      codeRaw?: string
    ): Promise<string> => {
      const lang = langRaw ?? "text";
      const code = codeRaw ?? "";

      try {
        return highlighter.codeToHtml(code, {
          lang,
          theme: "github-dark",
        });
      } catch {
        return highlighter.codeToHtml(code, {
          lang: "text",
          theme: "github-dark",
        });
      }
    }
  );

  const marked = new Marked();

  const html =  await marked.parse(processed);

  const safeHtml = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      "p", "strong", "em", "ul", "ol", "li", "br", "code", "pre", "span",
      "div", "blockquote", "hr", "table", "thead", "tbody", "tr", "th", "td"
    ],
    ALLOWED_ATTR: [
      "class", "style"
    ]
  });

  return safeHtml;
}

async function replaceAsync(
  str: string,
  regex: RegExp,
  asyncFn: (match: string, ...groups: (string | undefined)[]) => Promise<string>
): Promise<string> {
  const tasks: Promise<string>[] = [];
  const matches: string[] = [];

  str.replace(regex, (match: string, ...groups: string[]) => {
    matches.push(match);
    tasks.push(asyncFn(match, ...groups));
    return match;
  });

  const results = await Promise.all(tasks);

  let i = 0;
  return str.replace(regex, () => results[i++]);
}