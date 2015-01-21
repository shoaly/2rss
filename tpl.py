<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>{{rss_title}}</title>
    <link>{{source_url}}</link>
    <description>{{rss_title}}</description>
    <lastBuildDate>{{lastBuildDate}}</lastBuildDate>
    {{#items}}
      <item>
        <title>{{title}}</title>
        <link>{{link}}</link>
        

        <description>
          <![CDATA[
          {{{description}}}
          ]]>
        </description>
      </item>
    {{/items}}
  </channel>

</rss>

