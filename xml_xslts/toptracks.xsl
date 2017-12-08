<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:topTracks="http://www.topTracks.com/tracks#" xmlns:foaf="http://xmlns.com/foaf/spec/">

  <xsl:template match="/">
    <rdf:RDF>
      <rdf:Description rdf:about="http://www.topTracks.com/tracks">
        <xsl:apply-templates/>
      </rdf:Description>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="track">
    <xsl:variable name="mbid"><xsl:value-of select="mbid"/></xsl:variable>
    <xsl:variable name="imgSmall"><xsl:value-of select="image[@size='small']"/></xsl:variable>
    <xsl:variable name="imgMedium"><xsl:value-of select="image[@size='medium']"/></xsl:variable>
    <xsl:variable name="imgLarge"><xsl:value-of select="image[@size='large']"/></xsl:variable>
    <xsl:variable name="imgExtraLarge"><xsl:value-of select="image[@size='extralarge']"/></xsl:variable>

    <topTracks:track>
      <rdf:Description rdf:about="http://www.topTracks.com/tracks/{$mbid}">
        <foaf:name><xsl:value-of select="name"/></foaf:name>
        <topTracks:listeners><xsl:value-of select="listeners"/></topTracks:listeners>
        <topTracks:duration><xsl:value-of select="duration"/></topTracks:duration>
        <topTracks:url><xsl:value-of select="url"/></topTracks:url>
        <topTracks:imgSmall><xsl:value-of select="$imgSmall"/></topTracks:imgSmall>
        <topTracks:imgMedium><xsl:value-of select="$imgMedium"/></topTracks:imgMedium>
        <topTracks:imgLarge><xsl:value-of select="$imgLarge"/></topTracks:imgLarge>
        <topTracks:imgExtraLarge><xsl:value-of select="$imgExtraLarge"/></topTracks:imgExtraLarge>

        <xsl:for-each select="artist">
          <topTracks:artist>
            <rdf:Description rdf:about="http://www.topTracks.com/tracks/artist">
              <foaf:name_artist><xsl:value-of select="name"/></foaf:name_artist>
            </rdf:Description>
          </topTracks:artist>
        </xsl:for-each>
      </rdf:Description>
    </topTracks:track>
  </xsl:template>
</xsl:stylesheet>
