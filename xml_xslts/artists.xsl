<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:artist="http://www.artists.com/artist#" xmlns:foaf="http://xmlns.com/foaf/spec/">

  <xsl:template match="/">
    <rdf:RDF>
      <rdf:Description rdf:about="http://www.artists.com/artist ">
        <xsl:apply-templates/>
      </rdf:Description>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="artist">
    <xsl:variable name="name"><xsl:value-of select="name"/></xsl:variable>



    <xsl:variable name="imgSmall"><xsl:value-of select="image[@size='small']"/></xsl:variable>
    <xsl:variable name="imgMedium"><xsl:value-of select="image[@size='medium']"/></xsl:variable>
    <xsl:variable name="imgLarge"><xsl:value-of select="image[@size='large']"/></xsl:variable>
    <xsl:variable name="imgExtraLarge"><xsl:value-of select="image[@size='extralarge']"/></xsl:variable>

    <artist:artist>
      <rdf:Description rdf:about="http://www.artists.com/artist/{$name}">
        <foaf:name><xsl:value-of select="name"/></foaf:name>
        <artist:listeners><xsl:value-of select="listeners"/></artist:listeners>
        <artist:imgSmall><xsl:value-of select="$imgSmall"/></artist:imgSmall>
        <artist:imgMedium><xsl:value-of select="$imgMedium"/></artist:imgMedium>
        <artist:imgLarge><xsl:value-of select="$imgLarge"/></artist:imgLarge>
        <artist:imgExtraLarge><xsl:value-of select="$imgExtraLarge"/></artist:imgExtraLarge>

        <xsl:for-each select="album">
          <xsl:variable name="album"><xsl:value-of select="name"/></xsl:variable>
          <artist:album>
            <rdf:Description rdf:about="http://www.artists.com/artist/{$name}/album/{$album}">
              <foaf:name_album><xsl:value-of select="name"/></foaf:name_album>
              <artist:artist_name><xsl:value-of select="artist"/></artist:artist_name>
              <artist:album_listeners><xsl:value-of select="listeners"/></artist:album_listeners>
              <artist:wiki><xsl:value-of select="wiki/summary"/></artist:wiki>
              <artist:imgSmall_album><xsl:value-of select="image[@size='small']"/></artist:imgSmall_album>
              <artist:imgMedium_album><xsl:value-of select="image[@size='medium']"/></artist:imgMedium_album>
              <artist:imgLarge_album><xsl:value-of select="image[@size='large']"/></artist:imgLarge_album>
              <artist:imgExtraLarge_album><xsl:value-of select="image[@size='extralarge']"/></artist:imgExtraLarge_album>

              <xsl:for-each select="tracks/track">
                <xsl:variable name="track"><xsl:value-of select="name"/></xsl:variable>
                <artist:tracks>
                  <rdf:Description rdf:about="http://www.artists.com/artist/{$name}/album/{$album}/tracks/{$track}">
                    <foaf:track_name><xsl:value-of select="name"/></foaf:track_name>
                    <artist:track_duration><xsl:value-of select="duration"/></artist:track_duration>
                    <artist:artist_name><xsl:value-of select="artist/name"/></artist:artist_name>
                  </rdf:Description>
                </artist:tracks>
              </xsl:for-each>

              <xsl:for-each select="tags/tag">
                <xsl:variable name="tag"><xsl:value-of select="name"/></xsl:variable>
                <artist:tag>
                  <rdf:Description rdf:about="http://www.artists.com/artist/{$name}/album/{$album}/tags/tag/{$tag}">
                    <foaf:tag_name><xsl:value-of select="name"/></foaf:tag_name>
                  </rdf:Description>
                </artist:tag>
              </xsl:for-each>
            </rdf:Description>
          </artist:album>
        </xsl:for-each>
        <xsl:for-each select="bio">
          <artist:bio>
            <rdf:Description rdf:about="http://www.artists.com/artist/{$name}/bio">
              <foaf:bioSummary><xsl:value-of select="summary"/></foaf:bioSummary>
            </rdf:Description>
          </artist:bio>
        </xsl:for-each>
      </rdf:Description>
    </artist:artist>
  </xsl:template>

</xsl:stylesheet>
