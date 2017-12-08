<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:artist="http://www.artist.com/artists#" xmlns:foaf="http://xmlns.com/foaf/spec/">

  <xsl:template match="/">
    <rdf:RDF>
      <rdf:Description rdf:about="http://www.artists.com/artists">
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
    <xsl:variable name="alb_imgSmall"><xsl:value-of select="album/image[@size='small']"/></xsl:variable>
    <xsl:variable name="alb_imgMedium"><xsl:value-of select="album/image[@size='medium']"/></xsl:variable>
    <xsl:variable name="alb_imgLarge"><xsl:value-of select="album/image[@size='large']"/></xsl:variable>
    <xsl:variable name="alb_imgExtraLarge"><xsl:value-of select="album/image[@size='extralarge']"/></xsl:variable>

    <artist:artist>
      <rdf:Description rdf:about="http://www.artists.com/artists/{$name}">
        <foaf:name><xsl:value-of select="name"/></foaf:name>
        <artist:listeners><xsl:value-of select="listeners"/></artist:listeners>
        <artist:imgSmall><xsl:value-of select="$imgSmall"/></artist:imgSmall>
        <artist:imgMedium><xsl:value-of select="$imgMedium"/></artist:imgMedium>
        <artist:imgLarge><xsl:value-of select="$imgLarge"/></artist:imgLarge>
        <artist:imgExtraLarge><xsl:value-of select="$imgExtraLarge"/></artist:imgExtraLarge>

        <xsl:for-each select="album">
          <artist:album>
            <rdf:Description rdf:about="http://www.artists.com/album">
              <foaf:name_album><xsl:value-of select="name"/></foaf:name_album>
              <artist:artist_name><xsl:value-of select="artist"/></artist:artist_name>
              <artist:listeners><xsl:value-of select="listeners"/></artist:listeners>
              <artist:wiki><xsl:value-of select="wiki/summary"/></artist:wiki>
              <artist:imgSmall><xsl:value-of select="$alb_imgSmall"/></artist:imgSmall>
              <artist:imgMedium><xsl:value-of select="$alb_imgMedium"/></artist:imgMedium>
              <artist:imgLarge><xsl:value-of select="$alb_imgLarge"/></artist:imgLarge>
              <artist:imgExtraLarge><xsl:value-of select="$alb_imgExtraLarge"/></artist:imgExtraLarge>

              <xsl:for-each select="tracks/track">
                <artist:tracks>
                  <rdf:Description rdf:about="http://www.artists.com/album/tracks">
                    <foaf:track_name><xsl:value-of select="name"/></foaf:track_name>
                    <artist:track_duration><xsl:value-of select="duration"/></artist:track_duration>
                    <artist:artist_name><xsl:value-of select="artist/name"/></artist:artist_name>
                  </rdf:Description>
                </artist:tracks>
              </xsl:for-each>

              <xsl:for-each select="tags/tag">
                <artist:tag>
                  <rdf:Description rdf:about="http://www.artists.com/album/tags">
                    <foaf:tag_name><xsl:value-of select="name"/></foaf:tag_name>
                  </rdf:Description>
                </artist:tag>
              </xsl:for-each>
            </rdf:Description>
          </artist:album>
        </xsl:for-each>
      </rdf:Description>
    </artist:artist>
  </xsl:template>

</xsl:stylesheet>
