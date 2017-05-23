/*
 * This file configures MathJax, a JavaScript LaTeX renderer.
 * Full configuration information can be found here:
 *
 *     http://docs.mathjax.org/en/latest/configuration.html
 *
 * Principally, this file defines macros that MathJax will expand. The
 * TeX.Macros object maps macro names to LaTeX code.
 */
MathJax.Hub.Config({
    TeX: {
        Macros: {
            pT: 'p_{\\mathrm{T}}',
            HT: 'H_{\\mathrm{T}}',
            ET: 'E_{\\mathrm{T}}',
        }
    }
});
