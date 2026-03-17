import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import rehypeMermaid from 'rehype-mermaid';

export default defineConfig({
  site: 'https://your-org.github.io',
  base: '/appuracao',
  markdown: {
    rehypePlugins: [[rehypeMermaid, { strategy: 'img-svg' }]],
  },
  integrations: [
    starlight({
      title: 'Apuração Paralela',
      description: 'Contagem paralela e independente de votos via QR Code das urnas eletrônicas brasileiras.',
      defaultLocale: 'pt-BR',
      locales: {
        root: {
          label: 'Português (Brasil)',
          lang: 'pt-BR',
        },
      },
      customCss: ['./src/styles/custom.css'],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/your-org/appuracao' },
      ],
      sidebar: [
        { label: 'Sobre o Projeto', link: '/' },
        {
          label: 'Guia',
          items: [
            { label: 'Início Rápido', link: '/guia/inicio-rapido/' },
            { label: 'Estrutura do Repositório', link: '/guia/estrutura-repositorio/' },
          ],
        },
        {
          label: 'Arquitetura',
          items: [
            { label: 'Visão Geral', link: '/arquitetura/visao-geral/' },
            { label: 'Fluxo de Dados', link: '/arquitetura/fluxo-de-dados/' },
            { label: 'DynamoDB', link: '/arquitetura/dynamodb/' },
          ],
        },
        {
          label: 'Segurança',
          items: [
            { label: 'Modelo de Segurança', link: '/seguranca/modelo/' },
            { label: 'Checklist', link: '/seguranca/checklist/' },
          ],
        },
        {
          label: 'Infraestrutura',
          items: [
            { label: 'AWS SAM', link: '/infraestrutura/aws-sam/' },
            { label: 'Custos', link: '/infraestrutura/custos/' },
            { label: 'Templates VTL', link: '/infraestrutura/vtl-templates/' },
          ],
        },
        {
          label: 'Decisões',
          items: [
            { label: 'Decisões Técnicas', link: '/decisoes/decisoes-tecnicas/' },
          ],
        },
        {
          label: 'Roadmap',
          items: [
            { label: 'MVP', link: '/roadmap/mvp/' },
          ],
        },
      ],
    }),
  ],
});
